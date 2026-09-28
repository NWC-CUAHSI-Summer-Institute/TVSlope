"""3-gauge study-reach finder (self-contained; used by work6_3DHRS.ipynb).

For each SWOT reach it seeks THREE USGS gauges:
    * on-reach gauge  (<=1 km from the SWOT reach geometry)  -> DISCHARGE Q
    * upstream + downstream gauges (off-reach, same river via the SWORD reach chain) -> WSE -> twin-gauge SLOPE

Gauge->reach assignment is GEOGRAPHIC (spatial join to SWORD line geometry): the reach_id column in
paired_reach_SWOT_gage.csv is unreliable (a gauge can be assigned a reach 100 km away).

Selection criteria (documented for the slides):
  1. SWOT slope on the reach passes QC with n>=25 clean passes.
  2. on-reach gauge within 1 km of the SWOT reach geometry, with daily discharge.
  3. one upstream + one downstream gauge on the same-river SWORD chain (<=25 reach hops), each with stage+datum.
  4. twin-gauge span 3-70 km (brackets the reach without averaging over too long a stretch).
  5. |median twin slope| >= 100 mm/km (above the SWOT/altimetry noise floor).
  6. <=2 reaches per river (normalised name) for spatial spread; prefer higher SWOT n.

Writes output_exp6/reach3/reach3_selected.csv and returns it as a DataFrame."""
import warnings; warnings.filterwarnings("ignore")
import os; os.environ.pop("PROJ_DATA",None); os.environ.pop("PROJ_LIB",None)
import re
from pathlib import Path
from collections import defaultdict, Counter
import numpy as np, pandas as pd, pyogrio, urllib.request, urllib.parse
import dataretrieval.nwis as nwis, geopandas as gpd
def _resolve_root():
    """The data root, resolved per machine. Identical to the original wherever the original exists.

    1. $SLIPPERYSLOPE_ROOT   2. /Users/zixun/2026SI/slipperyslope   3. <repo>/slipperyslope
    Nothing in the science depends on which one is used; only on the tree being there."""
    import os as _os
    from pathlib import Path as _P
    env = _os.environ.get("SLIPPERYSLOPE_ROOT")
    if env:
        return _P(env)
    orig = _P("/Users/zixun/2026SI/slipperyslope")
    if orig.exists():
        return orig
    return _P(__file__).resolve().parent.parent / "slipperyslope"


ROOT=_resolve_root(); DATA=ROOT/"data"; DIS=DATA/"discharge"; TG=DATA/"twin_gauge"
SWORD=DATA/"SWORD_v17b_gpkg"/"na_sword_reaches_v17b.gpkg"; OUT=ROOT/"output_exp6"/"reach3"; OUT.mkdir(parents=True,exist_ok=True)
TG.mkdir(parents=True,exist_ok=True); DIS.mkdir(parents=True,exist_ok=True)
FT,CFS=0.3048,0.028316846592

# curated all-on-reach study reaches (the classic multi-gauge reaches: 3 USGS gauges ON one SWOT reach).
# (reach, river, gup[WSE], gmid[map], gdn[WSE], gq[discharge], span_m). up/dn give the twin slope; gq the discharge.
CURATED=[("73260900321","Chattahoochee, GA","02335880","02335990","02336000","02336000",5542.5),
         ("74264300071","Cumberland R, Nashville","03431500","03431514","03431712","03431500",14768.0),
         ("74266400321","White R, Indianapolis","03353000","03352953","03353611","03353000",4191.0),
         ("78299700131","Snake R, Idaho Falls","13057155","13057155","13058529","13057155",3792.0)]

def _first(x):
    if pd.isna(x): return None
    s=str(x).split(); return s[0] if s and s[0].isdigit() and s[0]!="0" else None

def _discharge(g):
    c=DIS/f"station_{g}.csv"
    if c.exists():
        try: return pd.read_csv(c,parse_dates=["datetime"])
        except Exception: pass
    try:
        df,_=nwis.get_dv(sites=g,parameterCd=["00060","00065"],start="2010-01-01",end="2026-07-01"); df=df.reset_index()
        qc=next((x for x in df.columns if x.startswith("00060") and x.endswith("_Mean")),None); hc=next((x for x in df.columns if x.startswith("00065") and x.endswith("_Mean")),None)
        o=pd.DataFrame({"datetime":pd.to_datetime(df["datetime"]).dt.tz_localize(None)})
        o["discharge_cms"]=pd.to_numeric(df[qc],errors="coerce")*CFS if qc else np.nan; o["gauge_height_m"]=pd.to_numeric(df[hc],errors="coerce")*FT if hc else np.nan
        o=o.dropna(subset=["discharge_cms"]); o.to_csv(c,index=False); return o
    except Exception: return pd.DataFrame()

def _stage(g):
    f0=TG/f"ser_{g}.csv"
    if f0.exists():
        d=pd.read_csv(f0,parse_dates=["date"])
        if "gh" in d and d.gh.notna().any(): return d[["date","gh"]].dropna()
    f=TG/f"dv2_{g}.csv"
    if f.exists(): return pd.read_csv(f,parse_dates=["date"])
    o=pd.DataFrame(columns=["date","gh"])
    try:
        df,_=nwis.get_dv(sites=g,parameterCd=["00065"],start="2015-01-01",end="2026-07-01"); df=df.reset_index()
        hc=next((x for x in df.columns if x.startswith("00065") and x.endswith("_Mean")),None)
        if hc: o=pd.DataFrame({"date":pd.to_datetime(df["datetime"]).dt.tz_localize(None),"gh":pd.to_numeric(df[hc],errors="coerce")*FT}).dropna(subset=["gh"])
    except Exception: pass
    o.to_csv(f,index=False); return o

_DC=TG/"_datum8.csv"; _dc={}
if _DC.exists():
    try: _dc.update(pd.read_csv(_DC,dtype={"site":str}).set_index("site").alt.to_dict())
    except Exception: pass
def _datum(g):
    if g in _dc and _dc[g]==_dc[g]: return _dc[g]
    v=np.nan
    for _ in range(3):
        try:
            u="https://waterservices.usgs.gov/nwis/site/?"+urllib.parse.urlencode({"format":"rdb","sites":g,"siteOutput":"expanded"})
            raw=urllib.request.urlopen(u,timeout=60).read().decode(); L=[l for l in raw.splitlines() if l and not l.startswith("#")]
            if len(L)>=3:
                cols=L[0].split("\t"); d=pd.DataFrame([dict(zip(cols,l.split("\t"))) for l in L[2:]]); a=pd.to_numeric(d.get("alt_va"),errors="coerce")
                if len(a) and pd.notna(a.iloc[0]): v=float(a.iloc[0])*FT
            break
        except Exception: continue
    _dc[g]=v
    try: pd.DataFrame([{"site":s,"alt":a} for s,a in _dc.items()]).to_csv(_DC,index=False)
    except Exception: pass
    return v

def gauge_to_reach():
    "GEOGRAPHIC gauge->reach via sjoin_nearest; cached to output_exp6/reach3/gauge2reach.csv."
    c=OUT/"gauge2reach.csv"
    if c.exists(): return pd.read_csv(c,dtype={"gage_id":str,"reach_id":str})
    pg=pd.read_csv(DATA/"paired_reach_SWOT_gage/paired_reach_SWOT_gage.csv",dtype={"gage_id":str},low_memory=False)
    g=pg.drop_duplicates("gage_id")[["gage_id","gage_latitude","gage_longitude"]].dropna()
    g["gage_latitude"]=pd.to_numeric(g.gage_latitude,errors="coerce"); g["gage_longitude"]=pd.to_numeric(g.gage_longitude,errors="coerce"); g=g.dropna()
    gpts=gpd.GeoDataFrame(g,geometry=gpd.points_from_xy(g.gage_longitude,g.gage_latitude),crs=4326).to_crs(5070)
    r=gpd.read_file(SWORD,columns=["reach_id"]).to_crs(5070); r["reach_id"]=r.reach_id.astype("int64").astype(str)
    j=gpd.sjoin_nearest(gpts,r[["reach_id","geometry"]],distance_col="dist_m").drop_duplicates("gage_id")
    out=j[["gage_id","reach_id","dist_m"]].copy(); out.to_csv(c,index=False); return out

def find(n=8, save=True, verbose=True):
    "return a DataFrame of n study reaches with the 3-gauge design + full data."
    from shapely.geometry import Point
    sw=pyogrio.read_dataframe(SWORD,columns=["reach_id","dist_out","rch_id_up","rch_id_dn"],read_geometry=False)
    sw["reach_id"]=sw.reach_id.astype("int64").astype(str)
    UP={r:_first(u) for r,u in zip(sw.reach_id,sw.rch_id_up)}; DN={r:_first(d) for r,d in zip(sw.reach_id,sw.rch_id_dn)}; DIST=dict(zip(sw.reach_id,sw.dist_out))
    pg=pd.read_csv(DATA/"paired_reach_SWOT_gage/paired_reach_SWOT_gage.csv",dtype={"reach_id":str,"gage_id":str},low_memory=False)
    for c in ["slope","reach_q","dark_frac","ice_clim_f"]: pg[c]=pd.to_numeric(pg[c],errors="coerce")
    g2r=gauge_to_reach(); g2r=g2r[g2r.dist_m<=1000].drop_duplicates("gage_id").set_index("gage_id")
    G=pg.drop_duplicates("gage_id").set_index("gage_id")[["gage_name","gage_latitude","gage_longitude"]].join(g2r[["reach_id"]],how="inner")
    reach2g=defaultdict(list)
    for gid,r in zip(G.index,G.reach_id): reach2g[r].append(gid)
    def walk(r,mp,K=25):
        out=[]; cur=r
        for _ in range(K):
            cur=mp.get(cur)
            if cur is None: break
            if cur in reach2g: out.append(cur)
        return out
    def medWSE(g):
        s=_stage(g); a=_datum(g); return (a+s.gh.median()) if len(s) and a==a else np.nan
    def geom(reach):
        try:
            gg=pyogrio.read_dataframe(SWORD,where=f"reach_id = {int(reach)}")
            return gg.set_crs(4326,allow_override=True).to_crs(5070) if len(gg) else None
        except Exception: return None
    cl=pg[(pg.reach_q<=1)&(pg.dark_frac.fillna(0)<=.5)&(pg.ice_clim_f.fillna(0)==0)&(pg.slope.abs().between(1e-6,1e-2))]
    swotn=cl.groupby("reach_id").size(); cand=[r for r in swotn[swotn>=25].index if r in reach2g and r in DIST]
    # prefer reaches with >=3 on-reach gauges (try "all on the reach" first), then by SWOT n
    cand.sort(key=lambda r:(0 if len(reach2g[r])>=3 else 1,-swotn[r]))
    picked=[]; seen=Counter()
    for r in cand:
        if len(picked)>=n: break
        onr=reach2g[r]
        if len(onr)>=3:
            # BEST case: 3 gauges on the reach -> mid = middle by WSE, up/dn = extremes; span from geometry
            gs=[g for g in onr[:6] if medWSE(g)==medWSE(g)]
            if len(gs)<3: continue
            gs.sort(key=lambda g:-medWSE(g)); gup,gmid,gdn=gs[0],gs[len(gs)//2],gs[-1]
            gm=geom(r)
            if gm is None: continue
            line=gm.geometry.iloc[0]
            pu=gpd.GeoSeries([Point(G.loc[gup,"gage_longitude"],G.loc[gup,"gage_latitude"])],crs=4326).to_crs(5070).iloc[0]
            pdn=gpd.GeoSeries([Point(G.loc[gdn,"gage_longitude"],G.loc[gdn,"gage_latitude"])],crs=4326).to_crs(5070).iloc[0]
            span=abs(line.project(pu)-line.project(pdn)); minspan=500
        else:
            # mid = ON-reach gauge (discharge); up/dn = off-reach chain gauges (WSE -> slope)
            ug=walk(r,UP); dg=walk(r,DN)
            if not ug or not dg: continue
            gmid=onr[0]; g1,g2=reach2g[ug[0]][0],reach2g[dg[0]][0]; w1,w2=medWSE(g1),medWSE(g2)
            if w1!=w1 or w2!=w2: continue
            gup,gdn=(g1,g2) if w1>=w2 else (g2,g1); minspan=3000
            span=abs(DIST[G.loc[gup,"reach_id"]]-DIST[G.loc[gdn,"reach_id"]])
        if len({gup,gmid,gdn})<3: continue
        if span<minspan or span>70000: continue
        if not len(_discharge(gmid)): continue
        su=_stage(gup); sd=_stage(gdn); au=_datum(gup); ad=_datum(gdn)
        if not len(su) or not len(sd) or au!=au or ad!=ad: continue
        m=su.rename(columns={"gh":"gu"}).merge(sd.rename(columns={"gh":"gd"}),on="date"); m["S"]=((au+m.gu)-(ad+m.gd))/span
        if len(m)<50 or abs(m.S.median())*1e6<100: continue
        nm=str(G.loc[gmid,"gage_name"]).upper().replace(".","")
        mt=re.search(r"([A-Z]+)\s+(RIVER|RV|R|CREEK|CK|CANAL|BAYOU)\b",nm); key=mt.group(1) if mt else nm.split()[0]
        if seen[key]>=2: continue
        seen[key]+=1
        riv=nm.split(" AT ")[0].split(" NEAR ")[0].split(" ABOVE ")[0].split(" BELOW ")[0].strip()[:24].title()
        picked.append(dict(reach=r,river=riv,gup=gup,gmid=gmid,gdn=gdn,gq=gmid,span_km=round(span/1000,1),
                           swot_n=int(swotn[r]),twin_n=len(m),twin_med_mmkm=round(m.S.median()*1e6,0),mode="on-reach + up/dn"))
        if verbose: print(f"  [{len(picked)}] {r} {riv[:20]:20s} up={gup} mid={gmid} dn={gdn} span={span/1000:.1f}km swot={swotn[r]} twinN={len(m)} med={m.S.median()*1e6:.0f}mm/km")
    # ---- curated all-on-reach reaches (3 gauges ON the reach; the classic multi-gauge study reaches) ----
    for reach,river,gup,gmid,gdn,gq,span in CURATED:
        try:
            cl2=pg[(pg.reach_id==reach)&(pg.reach_q<=1)&(pg.dark_frac.fillna(0)<=.5)&(pg.ice_clim_f.fillna(0)==0)&(pg.slope.abs().between(1e-6,1e-2))]
            su=_stage(gup); sd=_stage(gdn); au=_datum(gup); ad=_datum(gdn)
            m=su.rename(columns={"gh":"gu"}).merge(sd.rename(columns={"gh":"gd"}),on="date"); m["S"]=((au+m.gu)-(ad+m.gd))/span
            picked.append(dict(reach=reach,river=river,gup=gup,gmid=gmid,gdn=gdn,gq=gq,span_km=round(span/1000,1),
                               swot_n=int(len(cl2)),twin_n=len(m),twin_med_mmkm=round(m.S.median()*1e6,0),mode="all-on-reach"))
            if verbose: print(f"  [+] {reach} {river[:20]:20s} up={gup} mid={gmid} dn={gdn} gq={gq} span={span/1000:.1f}km swot={len(cl2)} twinN={len(m)} med={m.S.median()*1e6:.0f}mm/km (curated)")
        except Exception as e:
            if verbose: print(f"  [+] {reach} curated FAILED: {str(e)[:60]}")
    sel=pd.DataFrame(picked)
    if save and len(sel): sel.to_csv(OUT/"reach3_selected.csv",index=False)
    return sel

_HUC=OUT/"gauge_huc8.csv"; _hc={}
if _HUC.exists():
    try: _hc.update(pd.read_csv(_HUC,dtype={"site":str,"huc8":str}).set_index("site").huc8.to_dict())
    except Exception: pass
def gauge_huc8(g):
    "8-digit HUC of a USGS gauge (from NWIS huc_cd; 12-digit codes truncated to 8). Cached."
    g=str(g)
    if g in _hc and isinstance(_hc[g],str) and _hc[g].isdigit(): return _hc[g]
    v=""
    for _ in range(3):
        try:
            u="https://waterservices.usgs.gov/nwis/site/?"+urllib.parse.urlencode({"format":"rdb","sites":g,"siteOutput":"expanded"})
            raw=urllib.request.urlopen(u,timeout=60).read().decode(); L=[l for l in raw.splitlines() if l and not l.startswith("#")]
            if len(L)>=3:
                cols=L[0].split("\t"); d=dict(zip(cols,L[2].split("\t"))); h=str(d.get("huc_cd","")).strip()
                if h.isdigit(): v=h[:8].zfill(8)
            break
        except Exception: continue
    _hc[g]=v
    try: pd.DataFrame([{"site":s,"huc8":h} for s,h in _hc.items()]).to_csv(_HUC,index=False)
    except Exception: pass
    return v

def enumerate_studyable(swot_min=25, validate=True, add_huc8=True, save=True, verbose=True,
                        csv_name="studyable_reaches.csv"):
    """Master table of EVERY SWOT reach that carries 2-3 *paired* USGS gauges — either several gauges ON the
    reach, or one on-reach gauge plus an upstream/downstream gauge on the same SWORD chain.

    TWO PASSES.  (1) CHEAP structural pass — no per-gauge network: n_gauges, gauge_ids, roles (up/mid/dn),
    max gauge span (projected coords), reach span, SWOT n, mode.  Up/down order comes from the SWORD
    `dist_out` (chain) or along-reach projection (all-on-reach), so no water-level fetch is needed.
    (2) OPTIONAL `validate` pass — fetches discharge + up/dn daily stage & NWIS datum, computes the median
    twin-gauge water-surface slope, and flags `studyable` = discharge present AND |median slope| >= 100 mm/km
    (SWOT/altimetry noise floor) AND span 0.3-70 km. Generalises find(): no <=2-per-river cap, no n limit,
    keeps 2-gauge reaches. Columns: reach, river, n_gauges, gauge_ids, roles, gup/gmid/gdn, gq, on_reach_n,
    max_span_km, span_km, swot_n, [twin_n, twin_med_mmkm, has_discharge, studyable], mode, huc8.
    Writes output_exp6/reach3/studyable_reaches.csv."""
    from shapely.geometry import Point
    sw=pyogrio.read_dataframe(SWORD,columns=["reach_id","dist_out","rch_id_up","rch_id_dn"],read_geometry=False)
    sw["reach_id"]=sw.reach_id.astype("int64").astype(str)
    UP={r:_first(u) for r,u in zip(sw.reach_id,sw.rch_id_up)}; DN={r:_first(d) for r,d in zip(sw.reach_id,sw.rch_id_dn)}; DIST=dict(zip(sw.reach_id,sw.dist_out))
    pg=pd.read_csv(DATA/"paired_reach_SWOT_gage/paired_reach_SWOT_gage.csv",dtype={"reach_id":str,"gage_id":str},low_memory=False)
    for c in ["slope","reach_q","dark_frac","ice_clim_f"]: pg[c]=pd.to_numeric(pg[c],errors="coerce")
    g2r=gauge_to_reach(); g2r=g2r[g2r.dist_m<=1000].drop_duplicates("gage_id").set_index("gage_id")
    G=pg.drop_duplicates("gage_id").set_index("gage_id")[["gage_name","gage_latitude","gage_longitude"]].join(g2r[["reach_id"]],how="inner")
    reach2g=defaultdict(list)
    for gid,r in zip(G.index,G.reach_id): reach2g[r].append(gid)
    def walk(r,mp,K=25):
        cur=r
        for _ in range(K):
            cur=mp.get(cur)
            if cur is None: return None
            if cur in reach2g: return cur
        return None
    _P={}
    def pt5070(g):
        if g not in _P: _P[g]=gpd.GeoSeries([Point(G.loc[g,"gage_longitude"],G.loc[g,"gage_latitude"])],crs=4326).to_crs(5070).iloc[0]
        return _P[g]
    def proj_on_reach(reach,gs):
        "order on-reach gauges along the reach centerline (upstream first); returns (ordered, span_m)."
        try:
            gg=pyogrio.read_dataframe(SWORD,where=f"reach_id = {int(reach)}")
            line=gg.set_crs(4326,allow_override=True).to_crs(5070).geometry.iloc[0]
            d={g:line.project(pt5070(g)) for g in gs}; o=sorted(gs,key=lambda g:-d[g])   # larger proj = upstream
            return o, abs(d[o[0]]-d[o[-1]])
        except Exception:
            o=sorted(gs,key=lambda g:-pt5070(g).y); return o, max_span(o)
    def max_span(gs):
        ps=[pt5070(g) for g in gs]; return max(ps[i].distance(ps[j]) for i in range(len(ps)) for j in range(i+1,len(ps))) if len(ps)>=2 else 0.0
    def wser(g):
        s=_stage(g); a=_datum(g)
        return (pd.DataFrame({"date":s.date.values,"wse":a+s.gh.values}) if len(s) and a==a else pd.DataFrame(columns=["date","wse"]))
    def twin(ga,gb,span):
        wu=wser(ga).rename(columns={"wse":"wu"}); wd=wser(gb).rename(columns={"wse":"wd"})
        if not len(wu) or not len(wd) or not span: return np.nan,0
        m=wu.merge(wd,on="date"); m["S"]=(m.wu-m.wd)/span
        return (m.S.median(),len(m)) if len(m) else (np.nan,0)
    cl=pg[(pg.reach_q<=1)&(pg.dark_frac.fillna(0)<=.5)&(pg.ice_clim_f.fillna(0)==0)&(pg.slope.abs().between(1e-6,1e-2))]
    swotn=cl.groupby("reach_id").size()
    cand=[r for r in swotn[swotn>=swot_min].index if r in reach2g and r in DIST]
    cand.sort(key=lambda r:(0 if len(reach2g[r])>=2 else 1,-swotn[r]))
    # ---------- pass 1: cheap structural enumeration ----------
    picked=[]
    for r in cand:
        onr=reach2g[r]; gup=gmid=gdn=None; span=np.nan; mode=None; used=[]
        if len(onr)>=2:                                                # >=2 gauges ON the reach
            o,span=proj_on_reach(r,onr)
            gup,gdn=o[0],o[-1]; gmid=o[len(o)//2] if len(o)>=3 else None
            used=[g for g in [gup,gmid,gdn] if g]; mode="all-on-reach"
        else:                                                         # 1 on-reach gauge + up/dn chain (order by dist_out)
            on=onr[0]; ur=walk(r,UP); dr=walk(r,DN)
            ug=reach2g[ur][0] if ur else None; dg=reach2g[dr][0] if dr else None
            trip=[g for g in [ug,on,dg] if g]
            if len(trip)<2: continue
            trip.sort(key=lambda g:-DIST.get(G.loc[g,"reach_id"],0))    # upstream (larger dist_out) first
            gup,gdn=trip[0],trip[-1]; gmid=on if (len(trip)>=3 and on not in (gup,gdn)) else None
            span=abs(DIST.get(G.loc[gup,"reach_id"],0)-DIST.get(G.loc[gdn,"reach_id"],0))
            if not span or span!=span: span=pt5070(gup).distance(pt5070(gdn))
            used=[g for g in [gup,gmid,gdn] if g]; mode="on-reach + up/dn" if gmid else "on-reach + 1 neighbour"
        used=list(dict.fromkeys(used))
        if len(used)<2 or len(used)>3: continue
        if not span or span!=span or span<300 or span>70000: continue
        gq=next((g for g in [gmid,gup,gdn] if g and g in onr),onr[0])   # discharge gauge (prefer an on-reach gauge)
        nm=str(G.loc[gq,"gage_name"]).upper().replace(".","")
        riv=nm.split(" AT ")[0].split(" NEAR ")[0].split(" ABOVE ")[0].split(" BELOW ")[0].strip()[:24].title()
        picked.append(dict(reach=r,river=riv,n_gauges=len(used),gauge_ids=",".join(used),
                 roles=";".join(f"{lab}:{g}" for lab,g in [("up",gup),("mid",gmid),("dn",gdn)] if g),
                 gup=gup,gmid=(gmid or gq),gdn=gdn,gq=gq,on_reach_n=len(onr),
                 max_span_km=round(max_span(used)/1000,2),span_km=round(span/1000,1),
                 swot_n=int(swotn[r]),mode=mode))
    sel=pd.DataFrame(picked)
    if not len(sel): return sel
    sel=sel.sort_values(["n_gauges","swot_n"],ascending=[False,False]).reset_index(drop=True)
    if verbose: print(f"  pass 1: {len(sel)} reaches with 2-3 paired gauges "
                      f"({(sel['mode']=='all-on-reach').sum()} all-on-reach, {(sel['mode']!='all-on-reach').sum()} up/dn chain)")
    # ---------- pass 2: validate (both slope gauges have WSE + at least one gauge has discharge) ----------
    # The twin slope uses the two extreme WSE gauges (gup,gdn): twin_n>=30 => BOTH have WSE (so for a
    # 2-gauge reach both gauges carry WSE). The discharge gauge = ANY of the reach's gauges that has
    # discharge (prefer the on-reach gq); if only the non-gq gauge has it, gq is updated to that gauge.
    if validate:
        tw_med=[]; tw_n=[]; hasq=[]; dgq=[]
        for i,row in sel.iterrows():
            gids=[g for g in str(row.gauge_ids).split(",") if g]
            dq=next((g for g in [row.gq]+[g for g in gids if g!=row.gq] if len(_discharge(g))>0), None)
            Smed,tn=twin(row.gup,row.gdn,row.span_km*1000)
            hasq.append(dq is not None); dgq.append(dq or row.gq)
            tw_med.append(round(Smed*1e6,0) if Smed==Smed else np.nan); tw_n.append(int(tn))
            if verbose and (i+1)%25==0: print(f"    validated {i+1}/{len(sel)} ...")
        sel["gq"]=dgq                                              # discharge gauge = the one that actually has Q
        sel["has_discharge"]=hasq; sel["twin_n"]=tw_n; sel["twin_med_mmkm"]=tw_med
        # studyable: both slope gauges have WSE (twin_n) + a gauge has discharge + twin slope above the floor
        sel["studyable"]=sel.has_discharge & (sel.twin_n>=30) & (sel.twin_med_mmkm.abs()>=100)
        if verbose:
            _n2=int(((sel.n_gauges==2)&sel.studyable).sum()); _n3=int(((sel.n_gauges==3)&sel.studyable).sum())
            print(f"  pass 2: {int(sel.studyable.sum())} of {len(sel)} STUDYABLE "
                  f"({_n2} two-gauge [both WSE + one Q], {_n3} three-gauge; twin slope >= 100 mm/km over >=30 days)")
    if add_huc8:
        rows=sel[sel.studyable] if ("studyable" in sel and sel.studyable.any()) else sel
        if verbose: print(f"  fetching HUC8 for {len(rows)} reaches (NWIS huc_cd, cached) ...")
        h={}
        for g in rows.gq.unique(): h[g]=gauge_huc8(g)
        sel["huc8"]=[h.get(g,"") for g in sel.gq]
    if save: sel.to_csv(OUT/csv_name,index=False)
    return sel

if __name__=="__main__":
    import sys
    if len(sys.argv)>1 and sys.argv[1]=="enumerate":
        print(enumerate_studyable().to_string(index=False))
    else:
        print(find().to_string(index=False))
