# FIM output + event-forcing resolution: locate each treatment's extent tif and the NWM forcing discharge.
from pathlib import Path
import numpy as np, pandas as pd
from final_config import ROOT
from fim_reach import FR

def reach_fids(a):
    aoi = FR._aoi_dir(str(a.fim_huc8).zfill(8))
    return {int(f) for f in FR.reach_feature_ids(aoi, [a.reach])} if aoi else set()
def forcing_csv(a):
    huc = str(a.fim_huc8).zfill(8); ddir = ROOT/"data"/"fimbox_out"/f"HUC{huc}"/"discharge-inputs"
    if a.fim_driver == "operational":                                     # post-2023 -> NWM operational forecast
        return ddir/"operational_flood.csv"
    d = pd.to_datetime(getattr(a, "fim_date", a.bench_date)).strftime("%Y%m%d")   # in-retro -> NWM retrospective
    for c in [ddir/f"NWM_{d}T0000.csv", ddir/f"NWM_{d}.csv", *sorted(ddir.glob(f"NWM_{d}*.csv"))]:
        if Path(c).exists(): return c
    return None
def mainstem(a):
    csv = forcing_csv(a)
    if csv is None or not Path(csv).exists(): return reach_fids(a), np.nan
    df = pd.read_csv(csv); qcol = "discharge_cms" if "discharge_cms" in df.columns else "discharge"
    df["feature_id"] = pd.to_numeric(df.feature_id, errors="coerce").astype("Int64")
    df[qcol] = pd.to_numeric(df[qcol], errors="coerce")
    fids = reach_fids(a); sub = df[df.feature_id.isin(fids)].dropna(subset=[qcol])
    if not len(sub): return fids, np.nan
    peak = sub.groupby("feature_id")[qcol].max()
    main = set(int(x) for x in peak[peak >= 0.5*peak.max()].index)
    return main, float(peak[peak.index.isin(main)].median())

def treatment_tifs(a):
    huc = str(a.fim_huc8).zfill(8); bd = getattr(a, "fim_date", a.bench_date)
    fb = ROOT/"data"/"fimbox_out"/f"HUC{huc}"/"fim-outputs"
    op = (a.fim_driver == "operational")                                  # post-2023: NWM-forecast-driven tifs
    d = {}
    for t in ["hfirissword_new", "swot_median", "swot_floodstage", "swot_maxwse"]:
        cand = [fb/f"reach{a.reach}_{t}_operational.tif"] if op else [fb/f"batch_{huc}_{bd}_{t}.tif"]
        p = next((c for c in cand if c.exists()), None)
        if p: d[t] = p
    if a.gauge_paired:
        tv = [fb/f"reach{a.reach}_gauge_timevarying_operational.tif", fb/f"reach{a.reach}_gauge_timevarying_inundation.tif"]
        p = next((c for c in tv if c.exists()), None)
        if p: d["gauge_timevarying"] = p
    return d
