"""Per-reach figure dossier for the 3-gauge study design (NO ICESat-2).
Each study reach has THREE USGS gauges:
    * on-reach gauge (gmid, <1 km from the SWOT reach)  -> DISCHARGE Q(t) + stage H(t)
    * upstream + downstream gauges (gup, gdn, off-reach, same river) -> WSE(t) -> TWIN-GAUGE SLOPE S(t)
SWOT gives the reach water-surface slope; it is paired to the on-reach discharge BY DATE.
Selection table = output_exp6/reach3/reach3_selected.csv (built by the finder / notebook).
Figures written to output_exp6/per_reach3/. Reuses cached NWIS data; downloads what is missing."""
import warnings; warnings.filterwarnings("ignore")
import os; os.environ.pop("PROJ_DATA",None); os.environ.pop("PROJ_LIB",None)
from pathlib import Path
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.lines import Line2D
from scipy.stats import spearmanr, theilslopes
from sklearn.linear_model import LinearRegression
import dataretrieval.nwis as nwis, urllib.request, urllib.parse
import geopandas as gpd, pyogrio
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


ROOT=_resolve_root(); DATA=ROOT/"data"
OUT=ROOT/"output_exp6"/"per_reach3"; OUT.mkdir(parents=True,exist_ok=True)
DIS=DATA/"discharge"; TG=DATA/"twin_gauge"; SWORD=DATA/"SWORD_v17b_gpkg"/"na_sword_reaches_v17b.gpkg"
FT,CFS,FLOOR=0.3048,0.028316846592,100.0
plt.rcParams.update({"figure.dpi":110,"font.size":12,"axes.titlesize":13,"axes.labelsize":12,"axes.grid":True,"grid.alpha":.3})
SCM="plasma"                       # warm, perceptually-uniform slope colour map (bright = steeper)
UPC,MIDC,DNC="#1f77b4","#e53935","#2ca02c"
try: import contextily as cx; HAVE_CX=True
except Exception: HAVE_CX=False

# ---- SWOT slope table (reach_id keyed) + gauge coordinates ----
pg=pd.read_csv(DATA/"paired_reach_SWOT_gage/paired_reach_SWOT_gage.csv",dtype={"reach_id":str,"gage_id":str},low_memory=False)
NUM=["slope","slope2","slope_u","reach_q","dark_frac","ice_clim_f","xovr_cal_q","wse","xtrk_dist","gage_latitude","gage_longitude"]
for c in NUM: pg[c]=pd.to_numeric(pg.get(c),errors="coerce")
GC=pg.drop_duplicates("gage_id").set_index("gage_id")[["gage_name","gage_latitude","gage_longitude"]]
def gname(g): return str(GC.loc[g,"gage_name"]) if g in GC.index else g

SEL=pd.read_csv(OUT.parent/"reach3"/"reach3_selected.csv",dtype={"reach":str,"gup":str,"gmid":str,"gdn":str,"gq":str})
SEL["span_m"]=SEL["span_km"].astype(float)*1000

def TITLE(row,extra=""): return f"{row.river} — {row.reach}"+(f"  ·  {extra}" if extra else "")
def save(fig,name): fig.savefig(OUT/name,dpi=120,bbox_inches="tight"); plt.close(fig)

# ---- SWOT slope: QC + per-reach sign correction ----
def swot_clean(reach):
    s=pg[pg.reach_id==reach].copy()
    if not len(s): return pd.DataFrame()
    s["date"]=pd.to_datetime(s.get("SWOT_time"),utc=True,errors="coerce").dt.tz_localize(None); s=s.dropna(subset=["slope","date"])
    s=s[(s.wse.fillna(0)>-1e9)&(s.reach_q.fillna(9)<=1)&(s.dark_frac.fillna(0)<=.5)&(s.ice_clim_f.fillna(0)==0)&(s.xovr_cal_q.fillna(0)<=1)]
    if s.xtrk_dist.notna().any(): s=s[s.xtrk_dist.abs().between(10000,60000)|s.xtrk_dist.isna()]
    s=s[s.slope.abs().between(1e-6,1e-2)]
    if not len(s): return s.assign(slope_c=[])
    sign=np.sign(np.median(s.slope)); s["slope_c"]=s.slope*sign; s["slope2c"]=s.get("slope2")*sign
    s=s[s.slope_c>0].sort_values("date")
    # Lui-2026 outlier cut: keep slopes within 0.1x .. 10x the reach median. This preserves the natural
    # per-pass variability (low-slope dips at high flow) instead of the tight MAD 3.5sigma band, which
    # over-clipped tightly-clustered reaches and made the time series look artificially flat.
    if len(s)>=8:
        med=s.slope_c.median()
        if med>0: s=s[s.slope_c.between(0.1*med,10*med)]
    return s

# ---- NWIS daily discharge + stage (on-reach gauge), cached ----
def _iv_daily(g, param, scale):
    """Daily mean of the INSTANTANEOUS (IV) record for `param`, used as a fallback when the daily DV series is
    absent — as on large rivers (e.g. the Mississippi) that publish stage/discharge only as instantaneous values.
    Returns DataFrame(date, val) in SI (val already scaled)."""
    try:
        iv,_=nwis.get_iv(sites=g,parameterCd=[param],start="2015-01-01",end="2026-07-01"); iv=iv.reset_index()
        vc=next((c for c in iv.columns if c.startswith(param) and not c.endswith("_cd")),None)
        if not vc: return pd.DataFrame(columns=["date","val"])
        dt=pd.to_datetime(iv["datetime"],utc=True).dt.tz_localize(None)
        d=pd.DataFrame({"date":dt.dt.floor("D"),"val":pd.to_numeric(iv[vc],errors="coerce")*scale}).dropna(subset=["val"])
        return d.groupby("date",as_index=False).val.mean()
    except Exception:
        return pd.DataFrame(columns=["date","val"])

def discharge(g):
    if g is None or (isinstance(g,float) and g!=g): return pd.DataFrame()
    c=DIS/f"station_{g}.csv"
    if c.exists():
        try:
            d=pd.read_csv(c,parse_dates=["datetime"])
            if len(d): return d                                   # ignore a stale empty cache so the IV fallback can run
        except Exception: pass
    try:
        df,_=nwis.get_dv(sites=g,parameterCd=["00060","00065"],start="2010-01-01",end="2026-07-01"); df=df.reset_index()
        qc=next((x for x in df.columns if x.startswith("00060") and x.endswith("_Mean")),None)
        hc=next((x for x in df.columns if x.startswith("00065") and x.endswith("_Mean")),None)
        o=pd.DataFrame({"datetime":pd.to_datetime(df["datetime"]).dt.tz_localize(None)})
        o["discharge_cms"]=pd.to_numeric(df[qc],errors="coerce")*CFS if qc else np.nan
        o["gauge_height_m"]=pd.to_numeric(df[hc],errors="coerce")*FT if hc else np.nan
        o=o.dropna(subset=["discharge_cms"])
    except Exception:
        o=pd.DataFrame(columns=["datetime","discharge_cms","gauge_height_m"])
    if not len(o):                                                # DV discharge absent -> daily-mean the IV record
        dq=_iv_daily(g,"00060",CFS)
        if len(dq):
            o=dq.rename(columns={"date":"datetime","val":"discharge_cms"})
            dh=_iv_daily(g,"00065",FT); o=o.merge(dh.rename(columns={"date":"datetime","val":"gauge_height_m"}),on="datetime",how="left")
    if len(o):
        try: o.to_csv(c,index=False)
        except Exception: pass
    return o

# ---- daily stage series (for up/dn WSE): ser_ cache (daily-or-IV) -> dv2 -> get_dv ----
def stage_series(g):
    f0=TG/f"ser_{g}.csv"
    if f0.exists():
        d=pd.read_csv(f0,parse_dates=["date"])
        if "gh" in d and d.gh.notna().any(): return d[["date","gh"]].dropna().sort_values("date")
    f=TG/f"dv2_{g}.csv"
    if f.exists():
        d=pd.read_csv(f,parse_dates=["date"])
        if len(d): return d.sort_values("date")                   # ignore a stale empty cache so the IV fallback can run
    o=pd.DataFrame(columns=["date","gh"])
    try:
        df,_=nwis.get_dv(sites=g,parameterCd=["00065"],start="2015-01-01",end="2026-07-01"); df=df.reset_index()
        hc=next((x for x in df.columns if x.startswith("00065") and x.endswith("_Mean")),None)
        if hc: o=pd.DataFrame({"date":pd.to_datetime(df["datetime"]).dt.tz_localize(None),"gh":pd.to_numeric(df[hc],errors="coerce")*FT}).dropna(subset=["gh"])
    except Exception: pass
    if not len(o):                                                # DV daily stage absent (big rivers) -> daily-mean the IV record
        d=_iv_daily(g,"00065",FT)
        if len(d): o=d.rename(columns={"val":"gh"})
    o.to_csv(f,index=False); return o

_DC=TG/"_datum8.csv"; _dc={}
if _DC.exists():
    try: _dc.update(pd.read_csv(_DC,dtype={"site":str}).set_index("site").alt.to_dict())
    except Exception: pass
def datum(g):
    if g in _dc and _dc[g]==_dc[g]: return _dc[g]
    v=np.nan
    for _ in range(3):
        try:
            u="https://waterservices.usgs.gov/nwis/site/?"+urllib.parse.urlencode({"format":"rdb","sites":g,"siteOutput":"expanded"})
            raw=urllib.request.urlopen(u,timeout=60).read().decode(); L=[l for l in raw.splitlines() if l and not l.startswith("#")]
            if len(L)>=3:
                cols=L[0].split("\t"); d=pd.DataFrame([dict(zip(cols,l.split("\t"))) for l in L[2:]])
                a=pd.to_numeric(d.get("alt_va"),errors="coerce")
                if len(a) and pd.notna(a.iloc[0]): v=float(a.iloc[0])*FT
            break
        except Exception: continue
    _dc[g]=v
    try: pd.DataFrame([{"site":s,"alt":a} for s,a in _dc.items()]).to_csv(_DC,index=False)
    except Exception: pass
    return v

def wse_series(g):
    "daily water-surface elevation (m) = datum + gauge height."
    s=stage_series(g); a=datum(g)
    if not len(s) or a!=a: return pd.DataFrame(columns=["date","wse"])
    return pd.DataFrame({"date":s.date.values,"wse":a+s.gh.values})

def _span_m(row):
    "twin-gauge span in metres, from span_m if present else span_km*1000."
    s=getattr(row,"span_m",None)
    if s is None or (isinstance(s,float) and s!=s): s=float(getattr(row,"span_km",0) or 0)*1000
    return float(s)

def twin_series(row):
    "daily twin-gauge slope S(t)=(WSE_up-WSE_dn)/span, + on-reach discharge Q(t)."
    su=wse_series(row.gup).rename(columns={"wse":"wu"}); sd=wse_series(row.gdn).rename(columns={"wse":"wd"})
    if not len(su) or not len(sd) or not _span_m(row): return pd.DataFrame()
    m=su.merge(sd,on="date"); m["S"]=(m.wu-m.wd)/_span_m(row)
    if len(m)>20:
        lo,hi=m.S.quantile([.005,.995]); m=m[m.S.between(lo,hi)]
    gq=str(getattr(row,"gq","") or "").strip(); gq=gq if gq and gq.lower()!="nan" else row.gmid
    dis=discharge(gq)
    if len(dis): m=m.merge(dis.rename(columns={"datetime":"date"})[["date","discharge_cms"]],on="date",how="left")
    else: m["discharge_cms"]=np.nan
    return m.sort_values("date")

def pair_daily(sw,daily,col,tol="4D"):
    "attach nearest-day gauge value (col) to each SWOT overpass."
    if not len(sw) or not len(daily) or col not in daily: return sw.assign(**{col:np.nan})
    d=daily.dropna(subset=[col]).sort_values("date")[["date",col]]
    return pd.merge_asof(sw.sort_values("date"),d,on="date",direction="nearest",tolerance=pd.Timedelta(tol))

def robust_fit(x,y,frac=None,nbin=12,deg=3):
    """Polynomial slope-Q fit: a degree-`deg` polynomial (fit on standardised Q for stability) through the
    daily data, plus quantile-binned medians. Returns (xf,yf,label,r2,bx,by) or None. R² is vs the raw data.
    (frac is accepted for call-site compatibility and ignored.)"""
    x=np.asarray(x,float); y=np.asarray(y,float); m=np.isfinite(x)&np.isfinite(y); x,y=x[m],y[m]
    if len(x)<8: return None
    o=np.argsort(x); x,y=x[o],y[o]
    d=int(min(deg,max(1,len(np.unique(x))-1)))
    mu,sig=x.mean(),(x.std() or 1.0)
    c=np.polyfit((x-mu)/sig,y,d)                          # degree-d polynomial, standardised Q
    xf=np.linspace(x.min(),x.max(),200); yf=np.polyval(c,(xf-mu)/sig)
    yhat=np.polyval(c,(x-mu)/sig); ss=np.sum((y-np.mean(y))**2); r2=1-np.sum((y-yhat)**2)/ss if ss>0 else np.nan
    qs=np.quantile(x,np.linspace(0,1,nbin+1)); bx=[];by=[]
    for i in range(nbin):
        s=(x>=qs[i])&((x<=qs[i+1]) if i==nbin-1 else (x<qs[i+1]))
        if s.sum()>=3: bx.append(np.median(x[s])); by.append(np.median(y[s]))
    return xf,yf,f"degree-{d} polynomial (R²={r2:.2f})",r2,np.array(bx),np.array(by)

def swot_window(sw,pad_days=45):
    "min/max SWOT overpass date (+pad) for cropping time-series to the SWOT era."
    if not len(sw): return None,None
    return sw.date.min()-pd.Timedelta(days=pad_days), sw.date.max()+pd.Timedelta(days=pad_days)

# ==================================================================== figures
def make_reach(row):
    reach=row.reach; sw=swot_clean(reach)
    if len(sw)<8: return f"{reach}: skip (SWOT n={len(sw)})"
    gq=str(getattr(row,"gq","") or "").strip(); gq=gq if gq and gq.lower()!="nan" else row.gmid   # discharge gauge (may differ from map's mid)
    dis=discharge(gq)                                           # on-reach discharge+stage
    disH=dis.dropna(subset=["gauge_height_m"]) if len(dis) else dis
    Hmin=disH.gauge_height_m.min() if len(disH) else np.nan
    tw=twin_series(row)                                          # up/dn -> WSE -> slope
    # pair SWOT slope with on-reach discharge & stage & twin slope (by date)
    sp=pair_daily(sw,dis.rename(columns={"datetime":"date"}),"discharge_cms")
    sp=pair_daily(sp,dis.rename(columns={"datetime":"date"}),"gauge_height_m")
    if len(tw): sp=pair_daily(sp,tw[["date","S"]].rename(columns={"S":"Stwin"}),"Stwin",tol="6D")
    else: sp["Stwin"]=np.nan
    hasQ=sp.discharge_cms.notna().sum()>=8; hasH=sp.gauge_height_m.notna().sum()>=8
    snorm=LogNorm(vmin=max(sw.slope_c.quantile(.05),1e-6),vmax=sw.slope_c.quantile(.95))
    T2=sw.slope_c.median()
    rho,pv=spearmanr(sp.slope_c,sp.gauge_height_m) if hasH else (np.nan,np.nan)
    cls="backwater" if(rho<0 and pv<.05) else "kinematic" if(rho>0 and pv<.05) else "stable"

    # -- fig1: on-reach DISCHARGE + stage time series, SWOT dots coloured by slope --
    fig,axs=plt.subplots(2,1,figsize=(11,7),sharex=True); sc=None
    ax=axs[0]
    if len(dis): ax.plot(dis.datetime,dis.discharge_cms,lw=.6,color="#4a90d9",alpha=.7,label=f"USGS daily discharge · on-reach {gq}")
    if hasQ:
        d=sp.dropna(subset=["discharge_cms"]); sc=ax.scatter(d.date,d.discharge_cms,c=d.slope_c,cmap=SCM,norm=snorm,s=48,ec="k",lw=.4,zorder=5,label=f"SWOT overpass (colour=slope, n={len(d)})")
    ax.set_yscale("log"); ax.set_ylabel("discharge Q\n(cms, log)"); ax.legend(loc="upper left",fontsize=9)
    ax.set_title(TITLE(row,f"class: {cls.upper()}  ·  on-reach discharge, dots coloured by SWOT slope"),fontsize=12.5,fontweight="bold")
    ax=axs[1]
    if len(disH): ax.plot(disH.datetime,disH.gauge_height_m-Hmin,lw=.6,color="#2e8b57",label="gauge stage (on-reach)")
    if hasH:
        d=sp.dropna(subset=["gauge_height_m"]); s2=ax.scatter(d.date,d.gauge_height_m-Hmin,c=d.slope_c,cmap=SCM,norm=snorm,s=46,ec="k",lw=.35,zorder=5,label="stage at SWOT overpass (colour=slope)")
        if sc is None: sc=s2
    ax.set_ylabel("stage\n(m)"); ax.set_xlabel("date"); ax.legend(loc="upper left",fontsize=9)
    if sc is not None: fig.colorbar(sc,ax=axs,pad=.01,fraction=.03).set_label("SWOT water-surface slope (m/m, log)")
    save(fig,f"fig1_{reach}.png")

    # -- figWSE: upstream & downstream WSE time series (two lines) + twin-gauge slope; SWOT-era only --
    w0,w1=swot_window(sw)                                        # crop to the SWOT data window
    fig,axs=plt.subplots(2,1,figsize=(11,7.4),sharex=True)
    ax=axs[0]
    su=wse_series(row.gup); sd=wse_series(row.gdn)
    suw=su[su.date.between(w0,w1)] if len(su) and w0 is not None else su
    sdw=sd[sd.date.between(w0,w1)] if len(sd) and w0 is not None else sd
    tww=tw[tw.date.between(w0,w1)] if len(tw) and w0 is not None else tw
    if len(suw): ax.plot(suw.date,suw.wse,lw=.8,color=UPC,label=f"upstream WSE · {row.gup}")
    if len(sdw): ax.plot(sdw.date,sdw.wse,lw=.8,color=DNC,label=f"downstream WSE · {row.gdn}")
    ax.set_ylabel("water-surface\nelevation (m)"); ax.legend(loc="upper left",fontsize=9)
    ax.set_title(TITLE(row,f"up/down WSE → twin-gauge slope (span {row.span_km} km) · SWOT era"),fontsize=12.5,fontweight="bold")
    ax=axs[1]
    if len(tww):
        ax.plot(tww.date,tww.S*1e6,lw=.8,color="#8e44ad",label=f"twin-gauge slope (WSE$_{{up}}$−WSE$_{{dn}}$)/span, n={len(tww)}")
        ax.axhline(tw.S.median()*1e6,color="#5b2c6f",ls="--",lw=1.6,label=f"median {tw.S.median()*1e6:.0f} mm/km")
    if len(sw): ax.scatter(sw.date,sw.slope_c*1e6,s=30,color="#e67e22",ec="k",lw=.3,zorder=5,label="SWOT slope (per pass)")
    ax.axhline(FLOOR,color="grey",ls=":",lw=1.2,label="noise floor 100 mm/km")
    ax.set_ylabel("slope\n(mm/km)"); ax.set_xlabel("date"); ax.legend(loc="upper left",fontsize=8.5)
    if w0 is not None: ax.set_xlim(w0,w1)
    save(fig,f"figWSE_{reach}.png")

    # -- fig2b: SWOT slope vs on-reach discharge --
    fig,ax=plt.subplots(figsize=(7.2,6.6))
    if hasQ:
        d=sp.dropna(subset=["discharge_cms"]); ax.errorbar(d.discharge_cms,d.slope_c,yerr=(d.slope_u if d.slope_u.notna().any() else None),fmt="o",ms=5,color="#1f77b4",ecolor="#bcd",elinewidth=.8,capsize=2,mec="k",mew=.3,label="SWOT slope ±1σ (slope_u)")
        m=(d.discharge_cms>0)&(d.slope_c>0)
        if m.sum()>=5:
            bb,cc=np.polyfit(np.log10(d.discharge_cms[m]),np.log10(d.slope_c[m]),1); xf=np.logspace(np.log10(d.discharge_cms[m].min()),np.log10(d.discharge_cms[m].max()),40)
            ax.plot(xf,10**cc*xf**bb,"r-",lw=2,label=f"power-law S~Q$^{{{bb:.2f}}}$")
        # SWOT slope uncertainty = the reach-product slope_u (1σ); report the median and its fraction of the slope
        su=sw.slope_u.dropna()
        if len(su):
            frac=(sw.slope_u/sw.slope_c.abs()).median()*100
            ax.text(.03,.03,f"SWOT slope uncertainty (slope_u):\nmedian ±{su.median()*1e6:.0f} mm/km (1σ) ≈ {frac:.0f}% of slope",
                    transform=ax.transAxes,va="bottom",fontsize=9.5,bbox=dict(fc="#fff6e6",ec="#c9a227",lw=1))
        ax.set_xscale("log")
    else: ax.text(.5,.5,"no paired discharge",transform=ax.transAxes,ha="center")
    ax.set_yscale("log"); ax.set_xlabel("on-reach discharge Q (cms, log)"); ax.set_ylabel("SWOT slope S (m/m, log)")
    ax.set_title(TITLE(row,"slope vs discharge"),fontsize=12,fontweight="bold"); ax.legend(fontsize=9); save(fig,f"fig2b_slopeQ_{reach}.png")

    # -- fig56: Q–H rating + slope vs stage --
    fig,axs=plt.subplots(1,2,figsize=(13,6)); ax=axs[0]
    if len(disH): ax.scatter(dis.dropna(subset=["gauge_height_m"]).discharge_cms,disH.gauge_height_m-Hmin,s=5,alpha=.15,color="#2e8b57",label="full gauge record")
    if hasQ and hasH:
        d=sp.dropna(subset=["discharge_cms","gauge_height_m"]); ax.scatter(d.discharge_cms,d.gauge_height_m-Hmin,s=42,color="crimson",ec="k",lw=.3,zorder=5,label="SWOT-matched")
    ax.set_xscale("log"); ax.set_xlabel("discharge Q (cms, log)"); ax.set_ylabel("stage H (m)"); ax.set_title("rating curve  Q–H",fontsize=12); ax.legend(fontsize=9)
    ax=axs[1]
    if hasH:
        d=sp.dropna(subset=["gauge_height_m"]); H=d.gauge_height_m-Hmin; ax.scatter(H,d.slope_c,s=42,color="#4a7fb0",ec="k",lw=.3,label="SWOT")
        m=H>0
        if m.sum()>=5:
            bs,as_,_,_=theilslopes(np.log10(d.slope_c[m]),H[m]); xf=np.linspace(H[m].min(),H[m].max(),30); ax.plot(xf,10**(as_+bs*xf),"r-",lw=2,label="Theil-Sen fit")
        ax.text(.03,.97,f"rho={rho:.2f}  [{cls}]",transform=ax.transAxes,va="top",fontsize=10,bbox=dict(fc="white",ec="0.6"))
    ax.set_yscale("log"); ax.set_xlabel("stage H (m)"); ax.set_ylabel("slope S (m/m, log)"); ax.set_title("slope vs stage",fontsize=12); ax.legend(fontsize=9)
    fig.suptitle(TITLE(row),fontsize=13,fontweight="bold"); fig.tight_layout(); save(fig,f"fig56_{reach}.png")

    # -- fig7: 3-D rating surface Q=f(H,S) --
    if hasQ and hasH:
        d=sp.dropna(subset=["discharge_cms","gauge_height_m"]).copy(); d["H"]=d.gauge_height_m-Hmin+0.1
        d=d[(d.discharge_cms>0)&(d.slope_c>0)&(d.H>0)]
        if len(d)>=10:
            lQ=np.log10(d.discharge_cms.values); lH=np.log10(d.H.values); lS=np.log10(d.slope_c.values)
            C=LinearRegression().fit(np.column_stack([lH,lS]),lQ); r2=C.score(np.column_stack([lH,lS]),lQ)
            fig=plt.figure(figsize=(13,6)); ax=fig.add_subplot(1,2,1,projection="3d")
            hg=np.linspace(lH.min(),lH.max(),20); sg=np.linspace(lS.min(),lS.max(),20); HG,SG=np.meshgrid(hg,sg)
            QG=C.predict(np.column_stack([HG.ravel(),SG.ravel()])).reshape(HG.shape)
            ax.plot_surface(HG,SG,QG,cmap="viridis",alpha=.5,lw=0); ax.scatter(lH,lS,lQ,c=lQ,cmap="viridis",s=38,ec="k",lw=.3)
            ax.set_xlabel("log stage H"); ax.set_ylabel("log slope S"); ax.set_zlabel("log Q"); ax.view_init(elev=22,azim=-52); ax.set_title(f"Q=f(H,S) fit R²={r2:.2f}",fontsize=12)
            ax=fig.add_subplot(1,2,2)
            sc=ax.scatter(d.H,d.discharge_cms,c=d.slope_c,cmap="plasma",norm=LogNorm(),s=60,ec="k",lw=.4,label="SWOT obs (colour=slope)")
            fig.colorbar(sc,ax=ax,pad=.01).set_label("slope (m/m, log)"); ax.set_yscale("log"); ax.set_xlabel("stage H (m)"); ax.set_ylabel("Q (cms, log)"); ax.set_title("stage–discharge coloured by slope",fontsize=12); ax.legend(fontsize=9)
            fig.suptitle(TITLE(row,"3-D rating surface"),fontsize=13,fontweight="bold"); fig.tight_layout(); save(fig,f"fig7_{reach}.png")

    # -- slopeTS: SWOT slope vs gauge slope through time; SWOT-era only --
    w0,w1=swot_window(sw)
    tww=tw[tw.date.between(w0,w1)] if len(tw) and w0 is not None else tw
    fig,ax=plt.subplots(figsize=(9.5,6.6))
    if len(tww): ax.plot(tww.date,tww.S,lw=.9,color="#9a9a9a",zorder=1,label=f"gauge (twin-gauge) daily slope (n={len(tww)})")
    ax.plot(sw.date,sw.slope_c,"-o",color="#3b6ea5",ms=5,lw=1,mec="#25507f",zorder=3,label=f"SWOT slope per pass (n={len(sw)})")
    ax.axhline(T2,color="#a01e1e",ls="--",lw=2.2,zorder=2,label=f"SWOT median = {T2:.2e}")
    cv=sw.slope_c.std()/sw.slope_c.mean()
    ax.set_ylabel("water-surface slope (m/m)"); ax.set_xlabel("date")
    ax.set_title(TITLE(row,f"SWOT vs gauge slope through time (SWOT era)  ·  CV={cv:.2f}"),fontsize=12,fontweight="bold"); ax.legend(fontsize=9)
    if w0 is not None: ax.set_xlim(w0,w1)
    for lb in ax.get_xticklabels(): lb.set_rotation(30); lb.set_ha("right")
    save(fig,f"slopeTS_{reach}.png")

    # -- wss: SWOT WSS statistics --
    fig,ax=plt.subplots(figsize=(7,6)); S=sw.slope_c.values*1e6
    ax.hist(np.log10(S),bins=18,color="#69a",ec="k",alpha=.85)
    ax.axvline(np.log10(np.median(S)),color="r",ls="--",lw=2,label=f"median {np.median(S):.0f} mm/km")
    ax.axvline(2,color="purple",ls=":",lw=2,label="noise floor 100 mm/km")
    rngpct=(np.percentile(S,95)-np.percentile(S,5))/max(np.percentile(S,5),1e-9)*100
    ax.set_xlabel("log10 SWOT slope (mm/km)"); ax.set_ylabel("# passes")
    ax.set_title(TITLE(row,f"WSS stats: median {np.median(S):.0f} mm/km, range {rngpct:.0f}%, CV {cv:.2f}"),fontsize=11,fontweight="bold"); ax.legend(fontsize=9)
    save(fig,f"wss_{reach}.png")

    # -- gaugeSlopeQ: GAUGE (twin-gauge) slope vs discharge, polynomial fit --
    fig,ax=plt.subplots(figsize=(8.3,6.6))
    if len(tw):
        d=tw.dropna(subset=["discharge_cms"]); d=d[d.discharge_cms>0]; neg=int((d.S<=0).sum())
        if len(d):
            ax.scatter(d.discharge_cms,d.S*1e6,s=9,color="#7fa8d0",alpha=.4,ec="none",label=f"daily gauge slope (n={len(d)})")
            rf=robust_fit(d.discharge_cms.values,d.S.values*1e6)
            if rf:
                xf,yf,lab,r2,bx,by=rf
                ax.plot(xf,yf,"-",color="#c0392b",lw=2.8,zorder=5,label=lab)
                if len(bx): ax.plot(bx,by,"o",color="#7a1f1f",ms=7,mec="white",mew=.9,zorder=6,label="binned medians")
            # zoom the y-axis to the data so the slope–Q structure is visible; show the 100 mm/km floor only when relevant
            Smm=d.S.values*1e6; ylo,yhi=np.nanpercentile(Smm,[1,99]); pad=0.18*max(yhi-ylo,1); near=ylo<=FLOOR*3
            if near: ax.axhline(FLOOR,color="grey",ls=":",lw=1.1,alpha=.8,label="noise floor 100 mm/km"); ax.set_ylim(min(ylo-pad,FLOOR*.6),yhi+pad)
            else: ax.set_ylim(ylo-pad,yhi+pad)
            note=f"n={len(d)}, neg {100*neg/max(len(d),1):.0f}%, median {d.S.median()*1e6:.0f} mm/km"+("" if near else "  (≫ 100 mm/km floor)")
            ax.text(.03,.97,note,transform=ax.transAxes,va="top",fontsize=10.5,bbox=dict(fc="white",ec="0.6"))
    ax.set_xlabel("on-reach discharge Q (m$^3$/s)"); ax.set_ylabel("gauge (twin-gauge) slope S (mm/km)")
    ax.set_title(TITLE(row,"gauge slope vs discharge"),fontsize=12,fontweight="bold"); ax.legend(fontsize=9,loc="best"); save(fig,f"gaugeSlopeQ_{reach}.png")

    # -- swotVtwin: SWOT slope vs twin-gauge slope (validation) --
    fig,ax=plt.subplots(figsize=(8,6.6)); medmm=sw.slope_c.median()*1e6; tgm=tw.S.median()*1e6 if len(tw) else np.nan
    if len(tw):
        d=tw.dropna(subset=["discharge_cms"]); d=d[d.discharge_cms>0]
        if len(d):
            ax.scatter(d.discharge_cms,d.S*1e6,s=10,color="#c9c9c9",alpha=.5,ec="none",label="gauge (twin-gauge) truth")
            rf=robust_fit(d.discharge_cms.values,d.S.values*1e6)
            if rf: ax.plot(rf[0],rf[1],"--",color="#7f7f7f",lw=2.4,label="gauge fit (polynomial)")
    if hasQ:
        d=sp.dropna(subset=["discharge_cms"]); d=d[d.discharge_cms>0]; col="#d62728" if medmm<FLOOR else "#1f77b4"
        ax.scatter(d.discharge_cms,d.slope_c*1e6,s=52,color=col,alpha=.85,ec="k",lw=.5,label=f"SWOT slope (n={len(d)})")
        rf=robust_fit(d.discharge_cms.values,d.slope_c.values*1e6,deg=2)
        if rf: ax.plot(rf[0],rf[1],"-",color=col,lw=2.6,label="SWOT fit (polynomial)")
    rt=medmm/tgm if tgm==tgm and tgm else np.nan
    if medmm<FLOOR: v,vc="SWOT below noise floor","#c0392b"
    elif rt==rt and 0.5<=rt<=2: v,vc=f"SWOT ≈ gauge (ratio {rt:.2f})","#1e8a4e"
    elif rt==rt: v,vc=f"SWOT/gauge differ {rt:.1f}×","#b9770b"
    else: v,vc="sparse gauge","#b9770b"
    ax.text(.03,.03,"verdict: "+v,transform=ax.transAxes,fontsize=11,fontweight="bold",color=vc,va="bottom",bbox=dict(fc="white",ec=vc,lw=1.3))
    ax.set_xlabel("on-reach discharge Q (m$^3$/s)"); ax.set_ylabel("water-surface slope (mm/km)")
    ax.set_title(TITLE(row,"SWOT vs twin-gauge slope"),fontsize=12,fontweight="bold"); ax.legend(fontsize=9,loc="upper right"); save(fig,f"swotVtwin_{reach}.png")

    # -- map3: satellite + SWOT reach + 3 gauges --
    make_map(row)
    return f"{reach}: {row.river[:22]} SWOTn={len(sw)} twinN={len(tw)} [{cls}] Q={hasQ} H={hasH}"

def make_map(row):
    try:
        gg=pyogrio.read_dataframe(SWORD,where=f"reach_id = {int(row.reach)}")
        if not len(gg): return
        rr=gg.set_crs(4326,allow_override=True).to_crs(3857)
        pts=[("upstream",row.gup,UPC),("on-reach",row.gmid,MIDC),("downstream",row.gdn,DNC)]
        gp=gpd.GeoDataFrame(pd.DataFrame(pts,columns=["lab","g","col"]),
            geometry=gpd.points_from_xy([float(GC.loc[g,"gage_longitude"]) for _,g,_ in pts],[float(GC.loc[g,"gage_latitude"]) for _,g,_ in pts]),crs=4326).to_crs(3857)
        fig,ax=plt.subplots(figsize=(8,8.6)); rr.plot(ax=ax,color="#00e5ff",lw=2.6,zorder=4)
        for _,p in gp.iterrows():
            ax.scatter(p.geometry.x,p.geometry.y,s=175,marker="^",color=p.col,ec="white",lw=1.5,zorder=6)
            ax.annotate(f"{p.lab}\nUSGS {p.g}",(p.geometry.x,p.geometry.y),color="white",fontsize=9,fontweight="bold",xytext=(7,4),textcoords="offset points",zorder=7)
        b=rr.total_bounds; xs=list(gp.geometry.x)+[b[0],b[2]]; ys=list(gp.geometry.y)+[b[1],b[3]]
        cx0,cy0=(min(xs)+max(xs))/2,(min(ys)+max(ys))/2; half=max(max(xs)-min(xs),max(ys)-min(ys))/2*1.22+900
        ax.set_xlim(cx0-half,cx0+half); ax.set_ylim(cy0-half,cy0+half); ax.set_xticks([]); ax.set_yticks([])
        if HAVE_CX:
            try: cx.add_basemap(ax,source=cx.providers.Esri.WorldImagery,crs="EPSG:3857",attribution_size=5)
            except Exception: pass
        ax.legend(handles=[Line2D([],[],color="#00e5ff",lw=3,label="SWOT reach"),
            Line2D([],[],marker="^",color="w",mfc=UPC,mec="white",ms=12,label="upstream gauge → WSE"),
            Line2D([],[],marker="^",color="w",mfc=MIDC,mec="white",ms=12,label="on-reach gauge → discharge"),
            Line2D([],[],marker="^",color="w",mfc=DNC,mec="white",ms=12,label="downstream gauge → WSE")],loc="upper left",fontsize=9,framealpha=.88)
        ax.set_title(TITLE(row,f"3-gauge layout (span {row.span_km} km)"),fontsize=11.5,fontweight="bold")
        save(fig,f"map3_{row.reach}.png")
    except Exception as e: print(f"  {row.reach} map fail: {str(e)[:60]}")

# ==================================================================== grouped grids (all studyable reaches)
_RD={}
def reach_data(row, use_cache=True):
    """Shared per-reach data model for the montage panels: cleaned SWOT, on-reach discharge+stage,
    twin-gauge slope, and SWOT overpasses paired (by date) to discharge/stage/twin-slope. Memoised by
    reach id so the three relationship montages don't recompute it three times."""
    reach=str(row.reach)
    if use_cache and reach in _RD: return _RD[reach]
    sw=swot_clean(reach)
    gq=str(getattr(row,"gq","") or "").strip(); gq=gq if gq and gq.lower()!="nan" else str(getattr(row,"gmid",reach))
    dis=discharge(gq); disH=dis.dropna(subset=["gauge_height_m"]) if len(dis) else dis
    Hmin=disH.gauge_height_m.min() if len(disH) else np.nan
    try:
        tw=twin_series(row) if all(getattr(row,k,None) is not None for k in ("gup","gdn")) else pd.DataFrame()
    except Exception:
        tw=pd.DataFrame()
    sp=pair_daily(sw,dis.rename(columns={"datetime":"date"}),"discharge_cms") if len(sw) else sw
    if len(sw): sp=pair_daily(sp,dis.rename(columns={"datetime":"date"}),"gauge_height_m")
    D=dict(reach=reach,gq=gq,sw=sw,dis=dis,disH=disH,Hmin=Hmin,tw=tw,sp=sp)
    if use_cache: _RD[reach]=D
    return D

def _paneltitle(row):
    return f"{getattr(row,'river','')} — {row.reach}"

def panel_slope_vs_stage(ax,row,D=None,fs=8):
    "SWOT water-surface slope vs on-reach stage (dynamic class via Spearman)."
    D=D or reach_data(row); sp=D["sp"]; Hmin=D["Hmin"]
    d=sp.dropna(subset=["gauge_height_m","slope_c"]) if len(sp) else sp
    n=len(d)
    if n>=5:
        H=(d.gauge_height_m-Hmin).values; S=d.slope_c.values*1e6
        ax.scatter(H,S,s=26,color="#4a7fb0",ec="k",lw=.3,zorder=4)
        rho,pv=spearmanr(H,S); cls="backwater" if(rho<0 and pv<.05) else "kinematic" if(rho>0 and pv<.05) else "stable"
        m=H>0
        if m.sum()>=5:
            b,a,_,_=theilslopes(np.log10(S[m]),H[m]); xf=np.linspace(H[m].min(),H[m].max(),30)
            ax.plot(xf,10**(a+b*xf),"r-",lw=1.8,zorder=5)
        ax.text(.03,.97,f"ρ={rho:+.2f} [{cls}]\nn={n}",transform=ax.transAxes,va="top",fontsize=fs,bbox=dict(fc="white",ec="0.6"))
    else: ax.text(.5,.5,f"n={n}\ninsufficient stage",transform=ax.transAxes,ha="center",va="center",fontsize=fs)
    ax.set_yscale("log"); ax.set_xlabel("stage above low water (m)",fontsize=fs); ax.set_ylabel("SWOT slope (mm/km)",fontsize=fs)
    ax.set_title(_paneltitle(row),fontsize=fs+1); ax.grid(alpha=.3); ax.tick_params(labelsize=fs-1)

def panel_stage_vs_discharge(ax,row,D=None,fs=8):
    "traditional rating curve: stage vs discharge (full gauge record + SWOT-matched, dots coloured by slope)."
    D=D or reach_data(row); sp=D["sp"]; Hmin=D["Hmin"]; disH=D["disH"]; dis=D["dis"]
    if len(disH):
        ax.scatter(dis.dropna(subset=["gauge_height_m"]).discharge_cms,disH.gauge_height_m-Hmin,s=4,alpha=.12,color="#2e8b57",zorder=1)
    d=sp.dropna(subset=["discharge_cms","gauge_height_m"]) if len(sp) else sp
    n=len(d)
    if n>=5:
        sc=ax.scatter(d.discharge_cms,d.gauge_height_m-Hmin,c=d.slope_c,cmap=SCM,norm=LogNorm(),s=30,ec="k",lw=.3,zorder=5)
        ax.text(.03,.97,f"n={n}",transform=ax.transAxes,va="top",fontsize=fs,bbox=dict(fc="white",ec="0.6"))
    else: ax.text(.5,.5,f"n={n}\nno SWOT-matched Q+H",transform=ax.transAxes,ha="center",va="center",fontsize=fs)
    ax.set_xscale("log"); ax.set_xlabel("discharge Q (cms, log)",fontsize=fs); ax.set_ylabel("stage H (m)",fontsize=fs)
    ax.set_title(_paneltitle(row),fontsize=fs+1); ax.grid(alpha=.3); ax.tick_params(labelsize=fs-1)

def panel_slope_vs_discharge(ax,row,D=None,fs=8):
    "SWOT water-surface slope vs on-reach discharge (power-law fit)."
    D=D or reach_data(row); sp=D["sp"]
    d=sp.dropna(subset=["discharge_cms","slope_c"]) if len(sp) else sp
    d=d[d.discharge_cms>0] if len(d) else d; n=len(d)
    if n>=5:
        ax.scatter(d.discharge_cms,d.slope_c*1e6,s=26,color="#1f77b4",ec="k",lw=.3,zorder=4)
        m=(d.discharge_cms>0)&(d.slope_c>0)
        if m.sum()>=5:
            b,c=np.polyfit(np.log10(d.discharge_cms[m]),np.log10(d.slope_c[m]),1)
            xf=np.logspace(np.log10(d.discharge_cms[m].min()),np.log10(d.discharge_cms[m].max()),40)
            ax.plot(xf,10**c*(xf**b)*1e6,"r-",lw=1.8,zorder=5); ax.text(.03,.03,f"S~Q$^{{{b:.2f}}}$",transform=ax.transAxes,va="bottom",fontsize=fs,bbox=dict(fc="#fff6e6",ec="#c9a227"))
        ax.text(.03,.97,f"n={n}",transform=ax.transAxes,va="top",fontsize=fs,bbox=dict(fc="white",ec="0.6"))
        ax.set_xscale("log")
    else: ax.text(.5,.5,f"n={n}\nno paired discharge",transform=ax.transAxes,ha="center",va="center",fontsize=fs)
    ax.set_yscale("log"); ax.set_xlabel("discharge Q (cms, log)",fontsize=fs); ax.set_ylabel("SWOT slope (mm/km)",fontsize=fs)
    ax.set_title(_paneltitle(row),fontsize=fs+1); ax.grid(alpha=.3); ax.tick_params(labelsize=fs-1)

_PANELS={"slope_vs_stage":(panel_slope_vs_stage,"SWOT slope vs stage"),
         "stage_vs_discharge":(panel_stage_vs_discharge,"stage vs discharge (rating curve; dots coloured by SWOT slope)"),
         "slope_vs_discharge":(panel_slope_vs_discharge,"SWOT slope vs discharge")}

def montage(rows, kind, ncols=3, nrows=4, out_dir=None, prefix="montage", show=False):
    """Grouped grid of one relationship (kind in _PANELS) across all `rows` (a DataFrame of study reaches),
    paginated ncols x nrows per page. Returns the list of saved PNG paths."""
    panel_fn,subtitle=_PANELS[kind]; out_dir=Path(out_dir or OUT); out_dir.mkdir(parents=True,exist_ok=True)
    rows=[r for _,r in rows.iterrows()] if hasattr(rows,"iterrows") else list(rows)
    per=ncols*nrows; pages=(len(rows)+per-1)//per; paths=[]
    for pg in range(pages):
        chunk=rows[pg*per:(pg+1)*per]
        fig,axs=plt.subplots(nrows,ncols,figsize=(ncols*4.3,nrows*3.7)); axs=np.atleast_1d(axs).ravel()
        for ax,row in zip(axs,chunk):
            try: panel_fn(ax,row)
            except Exception as e: ax.text(.5,.5,f"{row.reach}\nERR {str(e)[:40]}",transform=ax.transAxes,ha="center",va="center",fontsize=7); ax.set_axis_off()
        for ax in axs[len(chunk):]: ax.axis("off")
        ttl=f"{subtitle}  —  {len(rows)} studyable reaches"+(f"  (page {pg+1}/{pages})" if pages>1 else "")
        fig.suptitle(ttl,fontsize=13,fontweight="bold",y=1.0); fig.tight_layout()
        p=out_dir/(f"{prefix}_{kind}"+(f"_p{pg+1}" if pages>1 else "")+".png")
        fig.savefig(p,dpi=120,bbox_inches="tight"); paths.append(p)
        if show: plt.show()
        else: plt.close(fig)
    return paths

def montage_all(rows, ncols=3, nrows=4, out_dir=None, prefix="montage", show=False):
    "Build all three relationship grids (slope-vs-stage, stage-vs-discharge, slope-vs-discharge)."
    return {k:montage(rows,k,ncols=ncols,nrows=nrows,out_dir=out_dir,prefix=prefix,show=show) for k in _PANELS}

# ==================================================================== AOI overview (maps at the beginning)
def conus_overview(rows, highlight_reaches=None, save=None, show=True, title=None):
    """CONUS locator map of every studyable reach (marker at its on-reach discharge gauge), coloured by the
    number of paired gauges; the deep-dive study reaches are ringed. `rows` = a DataFrame with gq + n_gauges."""
    rows=rows.copy(); highlight_reaches=set(str(r) for r in (highlight_reaches or []))
    states=gpd.read_file(DATA/"us_states.gpkg").to_crs(4326)
    lons=[]; lats=[]; ng=[]; hl=[]
    for _,r in rows.iterrows():
        g=str(getattr(r,"gq","") or getattr(r,"gmid",""))
        if g not in GC.index: continue
        lo=float(GC.loc[g,"gage_longitude"]); la=float(GC.loc[g,"gage_latitude"])
        if not (np.isfinite(lo) and np.isfinite(la)): continue
        lons.append(lo); lats.append(la); ng.append(int(getattr(r,"n_gauges",2))); hl.append(str(r.reach) in highlight_reaches)
    fig,ax=plt.subplots(figsize=(13,7.6))
    states.boundary.plot(ax=ax,color="0.7",lw=.5,zorder=1)
    lons=np.array(lons); lats=np.array(lats); ng=np.array(ng); hl=np.array(hl)
    sc=ax.scatter(lons,lats,c=ng,cmap="viridis",vmin=2,vmax=3,s=42,ec="k",lw=.3,zorder=3)
    if hl.any(): ax.scatter(lons[hl],lats[hl],s=190,facecolors="none",edgecolors="#d62728",lw=1.8,zorder=4,label="deep-dive study reach")
    cb=fig.colorbar(sc,ax=ax,fraction=.03,pad=.01,ticks=[2,3]); cb.set_label("paired gauges on/near reach")
    ax.set_xlim(-126,-66); ax.set_ylim(24,50); ax.set_xlabel("lon"); ax.set_ylabel("lat")
    ax.set_title(title or f"Study areas — {len(lons)} SWOT reaches with 2-3 paired USGS gauges",fontsize=13,fontweight="bold")
    if hl.any(): ax.legend(loc="lower left",fontsize=10)
    ax.grid(alpha=.25)
    if save: fig.savefig(save,dpi=130,bbox_inches="tight")
    if show: plt.show()
    else: plt.close(fig)
    return fig

def map_montage(rows, ncols=3, out_dir=None, prefix="aoimap", show=True, title=None):
    """Grid of the per-reach satellite AOI maps (map3_<reach>.png; generated by make_map if missing)."""
    import matplotlib.image as mpimg
    out_dir=Path(out_dir or OUT); rows=[r for _,r in rows.iterrows()] if hasattr(rows,"iterrows") else list(rows)
    imgs=[]
    for row in rows:
        p=OUT/f"map3_{row.reach}.png"
        if not p.exists():
            try: make_map(row)
            except Exception as e: print(f"  map {row.reach} fail: {str(e)[:50]}")
        if p.exists(): imgs.append((row,p))
    if not imgs: print("  no AOI maps"); return None
    nrows=(len(imgs)+ncols-1)//ncols
    fig,axs=plt.subplots(nrows,ncols,figsize=(ncols*4.2,nrows*4.4)); axs=np.atleast_1d(axs).ravel()
    for ax,(row,p) in zip(axs,imgs):
        try: ax.imshow(mpimg.imread(p))
        except Exception: pass
        ax.set_axis_off()
    for ax in axs[len(imgs):]: ax.axis("off")
    fig.suptitle(title or f"AOI location maps — {len(imgs)} study reaches (SWOT reach + on/up/down gauges)",fontsize=13,fontweight="bold",y=1.0)
    fig.tight_layout()
    if out_dir: fig.savefig(out_dir/f"{prefix}_montage.png",dpi=110,bbox_inches="tight")
    if show: plt.show()
    else: plt.close(fig)
    return fig

def generate_all():
    rows=[]
    for _,row in SEL.iterrows():
        try: print("figs "+make_reach(row))
        except Exception as e: print(row.reach,"ERR",str(e)[:80])
    print("DONE_PERREACH3")

if __name__=="__main__":
    generate_all()
