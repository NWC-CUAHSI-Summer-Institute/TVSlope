# NWM operational-forecast FIM. Built on FIMbox (github.com/sdmlua/fimbox).
import os, sys, time, shutil, traceback, warnings
warnings.filterwarnings("ignore")
os.environ.pop("PROJ_DATA", None); os.environ.pop("PROJ_LIB", None)
from pathlib import Path
import numpy as np, pandas as pd
import geopandas as gpd, pyogrio

sys.path.insert(0, "/Users/zixun/2026SI/FIMBox_github/fimbox/src")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import fimbox
from fimbox import generateFIM
from fimbox._dask import _resolve_n_workers
import fimbox_uncalibrated as FU
NW = _resolve_n_workers()

ROOT = Path("/Users/zixun/2026SI/slipperyslope")
SWORD = ROOT/"data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg"
FB = ROOT/"data/fimbox_out"
st = pd.read_csv(ROOT/"output_exp6/select/slope_treatments.csv", dtype={"reach": str}).drop_duplicates("reach").set_index("reach")

TREATS = ["hfirissword_new", "swot_median", "swot_floodstage", "swot_maxwse"]   # static treatments the notebook scores
SLOPE_COL = {"hfirissword_new": "hfirissword_new_mmkm", "swot_median": "swot_median_mmkm",
             "swot_floodstage": "swot_floodstage_mmkm", "swot_maxwse": "swot_maxwse_mmkm"}

# out-of-retrospective (event year > 2022) reaches, each with its NWM-forecast forcing csv (operational_flood.csv).
# gp_fit = paired-gauge S(Q) fit (from the notebook, fimserve env) for the gauge time-varying treatment.
GROUPS = {
    "10170203": dict(reach="74295200111", gauge_paired=False, forecast_csv="16UTC_shortrange_20240623.csv"),         # Big Sioux 2024
    "05140101": dict(reach="74267300251", gauge_paired=True, forecast_csv="17UTC_shortrange_20250412.csv",           # Ohio 2025
                     gp_fit=dict(kind="quadratic",
                                 params=[1.4127036421854573e-11, -4.3517437989988225e-07, 0.003842662855386138],
                                 Q_range=(206.99614858752, 13252.284205056))),
}

def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)

def feature_ids(aoi, reach):
    streams = next((aoi/"watershed-data").glob("*_subset_streams.gpkg"), None)
    nwm = pyogrio.read_dataframe(streams, columns=["ID"]).to_crs(5070)
    g = pyogrio.read_dataframe(SWORD, where=f"reach_id={reach}").set_crs(4326, allow_override=True).to_crs(5070)
    rl = gpd.GeoDataFrame(geometry=[g.geometry.iloc[0]], crs=5070)
    j = gpd.sjoin_nearest(nwm, rl, distance_col="d", max_distance=1000.0)
    return set(int(x) for x in j.ID)

def rebuild_operational_flood(aoi, forecast_csv):
    raw = pd.read_csv(aoi/"discharge-inputs"/forecast_csv)
    col = "discharge_cms" if "discharge_cms" in raw.columns else "discharge"
    raw = raw.rename(columns={col: "discharge_cms"})
    raw["feature_id"] = pd.to_numeric(raw.feature_id, errors="coerce").astype("Int64")
    raw = raw.dropna(subset=["feature_id", "discharge_cms"])[["feature_id", "discharge_cms"]]
    raw.to_csv(aoi/"discharge-inputs"/"operational_flood.csv", index=False)
    return dict(zip(raw.feature_id.astype("int64"), raw.discharge_cms.astype(float)))

def restore_orig(aoi):
    for ht in (aoi/"watershed-data"/"branches").glob("*/hydroTable_*.csv"):
        o = ht.with_name(ht.name + ".orig")
        if o.exists(): shutil.copy2(o, ht)
        ht.with_suffix(".parquet").unlink(missing_ok=True)
    (aoi/"watershed-data"/"hydrotable.parquet").unlink(missing_ok=True)
    (aoi/"watershed-data"/"hydrotable.csv").unlink(missing_ok=True)

def swap_static(aoi, fids, slope_mm):
    s_new = slope_mm/1e6                                          # mm/km -> m/m
    for ht in (aoi/"watershed-data"/"branches").glob("*/hydroTable_*.csv"):
        base = pd.read_csv(ht.with_name(ht.name + ".orig"))
        fm = base["feature_id"].astype("int64").isin(fids).values
        if fm.any():
            qc = base.columns.get_loc("discharge_cms"); sc = base.columns.get_loc("SLOPE")
            so = base.loc[fm, "SLOPE"].values; ok = (so > 0) & (s_new > 0)
            if ok.any():
                idx = np.where(fm)[0][ok]
                base.iloc[idx, qc] = base.iloc[idx, qc].values * np.sqrt(s_new/so[ok])
                base.iloc[idx, sc] = s_new
        base.to_csv(ht, index=False)
        ht.with_suffix(".parquet").unlink(missing_ok=True)
    (aoi/"watershed-data"/"hydrotable.parquet").unlink(missing_ok=True)
    (aoi/"watershed-data"/"hydrotable.csv").unlink(missing_ok=True)

def _sfunc(fit):
    p = fit["params"]
    if fit["kind"] == "quadratic":
        return lambda q: float(np.clip(np.polyval(p, q), 1e-7, None))
    a, b, c = p
    return lambda q: float(np.clip(a*np.power(q, b)+c, 1e-7, None))

def swap_timevarying(aoi, fids, fit):
    sfunc = _sfunc(fit); q_lo, q_hi = fit["Q_range"]
    def solveQ(q_orig, s_old):
        q = float(q_orig)
        for _ in range(60):
            qc = min(max(q, q_lo), q_hi); s_new = sfunc(qc)
            q2 = q_orig*np.sqrt(max(s_new, 1e-9)/max(s_old, 1e-9))
            if abs(q2-q) <= 1e-4*max(q2, 1.0): q = q2; break
            q = 0.5*(q+q2)
        return q, sfunc(min(max(q, q_lo), q_hi))
    for ht in (aoi/"watershed-data"/"branches").glob("*/hydroTable_*.csv"):
        base = pd.read_csv(ht.with_name(ht.name + ".orig"))
        fm = base["feature_id"].astype("int64").isin(fids).values
        if fm.any():
            qc = base.columns.get_loc("discharge_cms"); sc = base.columns.get_loc("SLOPE")
            for i in np.where(fm)[0]:
                q_orig = float(base.iloc[i, qc]); s_old = float(base.iloc[i, sc])
                if q_orig > 0 and s_old > 0:
                    qn, sn = solveQ(q_orig, s_old); base.iloc[i, qc] = qn; base.iloc[i, sc] = sn
        base.to_csv(ht, index=False)
        ht.with_suffix(".parquet").unlink(missing_ok=True)
    (aoi/"watershed-data"/"hydrotable.parquet").unlink(missing_ok=True)
    (aoi/"watershed-data"/"hydrotable.csv").unlink(missing_ok=True)

def run_fim(aoi, tag):
    ddir = aoi/"discharge-inputs"; ddir.mkdir(exist_ok=True)
    fq = ddir/f"operational_{tag}.csv"
    shutil.copy2(ddir/"operational_flood.csv", fq)   # FULL-AOI per-feature forcing (same discharge for every treatment; only the injected SRC slope differs)
    res = generateFIM(aoi, n_workers=NW, depth=True).from_discharge_inputs(csv=str(fq))
    exts = [Path(getattr(r, "extent_path", "")) for r in (res or []) if getattr(r, "extent_path", None)]
    if exts: return exts[-1]
    tifs = sorted((aoi/"fim-outputs").glob("*inundation*.tif"), key=lambda p: p.stat().st_mtime)
    return tifs[-1] if tifs else None

def main():
    log(f"fimbox {getattr(fimbox,'__version__','?')} | OPERATIONAL (NWM forecast) regen | subdivision ON | calibration OFF")
    for huc, grp in GROUPS.items():
        aoi = FB/f"HUC{huc}"; reach = grp["reach"]
        if not (aoi/"watershed-data"/"_subdiv.done").exists():
            log(f"HUC{huc}: subdivided baseline (.orig) missing -- run regen_subdiv_fim.py first; skip"); continue
        try:
            fids = feature_ids(aoi, reach); qmap = rebuild_operational_flood(aoi, grp["forecast_csv"])
        except Exception as e:
            log(f"HUC{huc}: setup error {e}"); continue
        if not fids: log(f"HUC{huc}: no feature_ids, skip"); continue
        _qs = list(qmap.values()); log(f"HUC{huc} reach{reach}: {len(fids)} reach fids (slope-injected); FULL-AOI forcing = {len(qmap)} fids (median {np.median(_qs):,.0f} m3/s)")
        fo = aoi/"fim-outputs"
        for treat in TREATS:
            dest = fo/f"reach{reach}_{treat}_operational.tif"
            s = st.loc[reach, SLOPE_COL[treat]] if reach in st.index else np.nan
            if not (s == s and s > 0): log(f"  {treat}: no slope, skip"); continue
            t0 = time.time()
            try:
                swap_static(aoi, fids, s)
                ext = run_fim(aoi, treat)
                if ext and Path(ext).exists(): shutil.copy2(ext, dest); log(f"  {treat}: OK {time.time()-t0:.0f}s -> {dest.name}")
                else: log(f"  {treat}: no FIM extent ({time.time()-t0:.0f}s)")
            except Exception as e:
                log(f"  {treat}: ERROR {e}\n{traceback.format_exc()[-400:]}")
        if grp["gauge_paired"]:
            dest = fo/f"reach{reach}_gauge_timevarying_operational.tif"; t0 = time.time()
            try:
                swap_timevarying(aoi, fids, grp["gp_fit"])
                ext = run_fim(aoi, "gauge_timevarying")
                if ext and Path(ext).exists(): shutil.copy2(ext, dest); log(f"  gauge_timevarying: OK {time.time()-t0:.0f}s -> {dest.name}")
                else: log(f"  gauge_timevarying: no FIM extent ({time.time()-t0:.0f}s)")
            except Exception as e:
                log(f"  gauge_timevarying: ERROR {e}\n{traceback.format_exc()[-400:]}")
        restore_orig(aoi)                                        # leave the HUC on its subdivided baseline
    log("OPERATIONAL REGEN DONE")

if __name__ == "__main__":
    main()
