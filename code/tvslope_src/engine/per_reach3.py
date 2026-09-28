# Per-reach gauge coordinates + NWIS discharge/stage/WSE series and twin-gauge slope.
from pathlib import Path
from types import SimpleNamespace
import numpy as np, pandas as pd
import dataretrieval.nwis as nwis, urllib.request, urllib.parse
from final_config import DATA, CFS, FT, GC
DIS = DATA/"discharge"; TG = DATA/"twin_gauge"
def _iv_daily(g, param, scale):
    try:
        iv, _ = nwis.get_iv(sites=g, parameterCd=[param], start="2015-01-01", end="2026-07-01"); iv = iv.reset_index()
        vc = next((c for c in iv.columns if c.startswith(param) and not c.endswith("_cd")), None)
        if not vc: return pd.DataFrame(columns=["date", "val"])
        dt = pd.to_datetime(iv["datetime"], utc=True).dt.tz_localize(None)
        d = pd.DataFrame({"date": dt.dt.floor("D"), "val": pd.to_numeric(iv[vc], errors="coerce")*scale}).dropna(subset=["val"])
        return d.groupby("date", as_index=False).val.mean()
    except Exception:
        return pd.DataFrame(columns=["date", "val"])
def discharge(g):
    if g is None or (isinstance(g, float) and g != g): return pd.DataFrame()
    c = DIS/f"station_{g}.csv"
    if c.exists():
        try:
            d = pd.read_csv(c, parse_dates=["datetime"])
            if len(d): return d
        except Exception: pass
    try:
        df, _ = nwis.get_dv(sites=g, parameterCd=["00060", "00065"], start="2010-01-01", end="2026-07-01"); df = df.reset_index()
        qc = next((x for x in df.columns if x.startswith("00060") and x.endswith("_Mean")), None)
        hc = next((x for x in df.columns if x.startswith("00065") and x.endswith("_Mean")), None)
        o = pd.DataFrame({"datetime": pd.to_datetime(df["datetime"]).dt.tz_localize(None)})
        o["discharge_cms"] = pd.to_numeric(df[qc], errors="coerce")*CFS if qc else np.nan
        o["gauge_height_m"] = pd.to_numeric(df[hc], errors="coerce")*FT if hc else np.nan
        o = o.dropna(subset=["discharge_cms"])
    except Exception:
        o = pd.DataFrame(columns=["datetime", "discharge_cms", "gauge_height_m"])
    if not len(o):
        dq = _iv_daily(g, "00060", CFS)
        if len(dq):
            o = dq.rename(columns={"date": "datetime", "val": "discharge_cms"})
            dh = _iv_daily(g, "00065", FT); o = o.merge(dh.rename(columns={"date": "datetime", "val": "gauge_height_m"}), on="datetime", how="left")
    if len(o):
        try: o.to_csv(c, index=False)
        except Exception: pass
    return o
def stage_series(g):
    f0 = TG/f"ser_{g}.csv"
    if f0.exists():
        d = pd.read_csv(f0, parse_dates=["date"])
        if "gh" in d and d.gh.notna().any(): return d[["date", "gh"]].dropna().sort_values("date")
    f = TG/f"dv2_{g}.csv"
    if f.exists():
        d = pd.read_csv(f, parse_dates=["date"])
        if len(d): return d.sort_values("date")
    o = pd.DataFrame(columns=["date", "gh"])
    try:
        df, _ = nwis.get_dv(sites=g, parameterCd=["00065"], start="2015-01-01", end="2026-07-01"); df = df.reset_index()
        hc = next((x for x in df.columns if x.startswith("00065") and x.endswith("_Mean")), None)
        if hc: o = pd.DataFrame({"date": pd.to_datetime(df["datetime"]).dt.tz_localize(None), "gh": pd.to_numeric(df[hc], errors="coerce")*FT}).dropna(subset=["gh"])
    except Exception: pass
    if not len(o):
        d = _iv_daily(g, "00065", FT)
        if len(d): o = d.rename(columns={"val": "gh"})
    try: o.to_csv(f, index=False)
    except Exception: pass
    return o
# --- gauge datum elevations, harmonised onto one vertical datum -------------------------------
# NWIS reports alt_va against whatever alt_datum_cd says. Among this study's gauges that is
# NAVD88 for most, NGVD29 for a few, and absent for a handful -- and 7 twin-gauge pairs are
# split across two datums. Differencing those two gauges without converting folds the
# NGVD29<->NAVD88 offset (~0.1-0.2 m here, and spatially varying) straight into the
# water-surface slope. Over a 20-30 km span that is ~5-10 mm/km of pure artefact, the same
# order as the real signal. So the elevation is converted to datum.GAUGE_REF_DATUM on the way
# in, and a gauge whose datum is unusable (LOCAL / ASSUMED / missing) yields NaN rather than a
# number that silently poisons the pair.
import datum as _VD

_DC = TG/f"_datum8_{_VD.GAUGE_REF_DATUM}.csv"      # new schema; the old _datum8.csv lacked alt_datum_cd
_dc: dict[str, dict] = {}
if _DC.exists():
    try:
        _dc.update(pd.read_csv(_DC, dtype={"site": str}).set_index("site").to_dict("index"))
    except Exception: pass

def _fetch_site(g):
    """NWIS expanded site record -> (alt_va in metres, alt_datum_cd, lat, lon)."""
    for _ in range(3):
        try:
            u = "https://waterservices.usgs.gov/nwis/site/?"+urllib.parse.urlencode({"format": "rdb", "sites": g, "siteOutput": "expanded"})
            raw = urllib.request.urlopen(u, timeout=60).read().decode(); L = [l for l in raw.splitlines() if l and not l.startswith("#")]
            if len(L) >= 3:
                cols = L[0].split("\t"); d = pd.DataFrame([dict(zip(cols, l.split("\t"))) for l in L[2:]])
                a  = pd.to_numeric(d.get("alt_va"), errors="coerce")
                la = pd.to_numeric(d.get("dec_lat_va"), errors="coerce")
                lo = pd.to_numeric(d.get("dec_long_va"), errors="coerce")
                cd = d.get("alt_datum_cd")
                return (float(a.iloc[0])*FT if len(a) and pd.notna(a.iloc[0]) else np.nan,
                        str(cd.iloc[0]).strip() if cd is not None and len(cd) else "",
                        float(la.iloc[0]) if len(la) and pd.notna(la.iloc[0]) else np.nan,
                        float(lo.iloc[0]) if len(lo) and pd.notna(lo.iloc[0]) else np.nan)
            return np.nan, "", np.nan, np.nan
        except Exception: continue
    return np.nan, "", np.nan, np.nan

def datum_info(g):
    """Full harmonised datum record for a gauge, cached. Keys: alt, alt_raw, cd, lat, lon, note."""
    if g in _dc: return _dc[g]
    raw, cd, la, lo = _fetch_site(g)
    if raw != raw or la != la or lo != lo:
        rec = dict(alt=np.nan, alt_raw=raw, cd=cd, lat=la, lon=lo,
                   note="no alt_va / coordinates reported" if raw != raw else "no coordinates reported")
    else:
        h, note = _VD.gauge_elevation_to(lo, la, raw, cd, _VD.GAUGE_REF_DATUM)
        rec = dict(alt=h, alt_raw=raw, cd=cd, lat=la, lon=lo, note=note)
    _dc[g] = rec
    try:
        pd.DataFrame([{"site": k, **v} for k, v in _dc.items()]).to_csv(_DC, index=False)
    except Exception: pass
    return rec

def datum(g):
    """Gauge datum elevation in metres on datum.GAUGE_REF_DATUM (NaN if the datum is unusable)."""
    return datum_info(g)["alt"]

def wse_series(g):
    """Gauge water-surface elevation on datum.GAUGE_REF_DATUM."""
    s = stage_series(g); a = datum(g)
    if not len(s) or a != a: return pd.DataFrame(columns=["date", "wse"])
    return pd.DataFrame({"date": s.date.values, "wse": a+s.gh.values})
def _span_m(row):
    s = getattr(row, "span_m", None)
    if s is None or (isinstance(s, float) and s != s): s = float(getattr(row, "span_km", 0) or 0)*1000
    return float(s)
def twin_series(row):
    su = wse_series(row.gup).rename(columns={"wse": "wu"}); sd = wse_series(row.gdn).rename(columns={"wse": "wd"})
    if not len(su) or not len(sd) or not _span_m(row): return pd.DataFrame()
    m = su.merge(sd, on="date"); m["S"] = (m.wu-m.wd)/_span_m(row)
    if len(m) > 20:
        lo, hi = m.S.quantile([.005, .995]); m = m[m.S.between(lo, hi)]
    gq = str(getattr(row, "gq", "") or "").strip(); gq = gq if gq and gq.lower() != "nan" else row.gmid
    dis = discharge(gq)
    if len(dis): m = m.merge(dis.rename(columns={"datetime": "date"})[["date", "discharge_cms"]], on="date", how="left")
    else: m["discharge_cms"] = np.nan
    return m.sort_values("date")
P3  = SimpleNamespace(GC=GC, discharge=discharge, stage_series=stage_series, datum=datum, datum_info=datum_info, wse_series=wse_series, twin_series=twin_series)
