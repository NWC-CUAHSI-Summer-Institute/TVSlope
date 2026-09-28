# Stage/subdivide HAND, inject each slope, run the FIM (in-retrospective + gauge). Built on FIMbox (github.com/sdmlua/fimbox).
import os, sys, time, shutil, traceback, warnings
warnings.filterwarnings("ignore")
os.environ.pop("PROJ_DATA", None); os.environ.pop("PROJ_LIB", None)
from pathlib import Path
import numpy as np, pandas as pd
import geopandas as gpd, pyogrio

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fimbox
from fimbox import getAllInputData, BranchDerivation, AOIProcessingConfig, calculate_allbranches, generateFIM, getNWMretrospective
from fimbox._dask import _resolve_n_workers
import fimbox_uncalibrated as FU
import dataretrieval.nwis as nwis

ROOT = Path("/Users/zixun/2026SI/slipperyslope")
SWORD = ROOT/"data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg"
FB = ROOT/"data/fimbox_out"
CFS = 0.028316846592
NW = _resolve_n_workers()
st = pd.read_csv(ROOT/"output_exp6/select/slope_treatments.csv", dtype={"reach": str}).drop_duplicates("reach").set_index("reach")
ONLY = os.environ.get("ONLY_REACH")
FORCE = bool(os.environ.get("FORCE_FIM"))   # 1 -> overwrite existing tifs (full rebuild) instead of skipping

TREATS = ["baseline", "hfirissword_new", "swot_median", "swot_floodstage", "swot_maxwse"]
SLOPE_COL = {"baseline": "hydrofab_base_mmkm", "hfirissword_new": "hfirissword_new_mmkm", "swot_median": "swot_median_mmkm",
             "swot_floodstage": "swot_floodstage_mmkm", "swot_maxwse": "swot_maxwse_mmkm"}
# grouped by HUC so reaches sharing a HUC (Illinois 74282100111 + 74282100101 in 07130011) get JOINT slope
# injection into one HUC-wide batch tif (each reach is then scored in its own eval box by the notebook).
GROUPS = {
    "10170203": dict(reaches=["74295200111"], bench="2024-06-23", driver="gauge", gq={"74295200111": "06483950"}),  # Big Sioux 2024 (out of retro)
    "10230003": dict(reaches=["74295100321"], bench="2018-06-10", driver="nwm"),                                    # Little Sioux (needs staging)
    "07140105": dict(reaches=["74270100061"], bench="2017-05-04", driver="nwm"),                                    # Mississippi
    "05140101": dict(reaches=["74267300251"], bench="2025-04-12", driver="gauge", gq={"74267300251": "03294500"}),  # Ohio 2025 (out of retro)
    "07130011": dict(reaches=["74282100111", "74282100101"], bench="2016-01-04", driver="nwm"),                     # Illinois x2 (joint inject)
}
GAUGE_Q_FALLBACK = {"74267300251": 15631.0, "74295200111": 2973.0}   # Big Sioux fallback (its gauge-driven tif is unused, but avoids a NaN-discharge failure)

def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)

def aoi_dir_for(huc):
    d = FB/f"HUC{huc}"
    return d if (d/"watershed-data").is_dir() and list((d/"watershed-data").glob("*_subset_streams.gpkg")) else None

def stage_and_build(huc):
    aoi = aoi_dir_for(huc)
    if aoi is None:
        log(f"  HUC{huc}: staging (getAllInputData)...")
        getAllInputData(huc8=huc, out_dir=str(FB), buffer_m=2000.0, headwater_buffer_cells=8,
                        get_flowlines=True, get_catchments=True, resolution="medium", identifier="nwm").run()
        aoi = FB/f"HUC{huc}"
    wsd = aoi/"watershed-data"
    if not list((wsd/"branches").glob("*/hydroTable_*.csv")):        # build HAND only if not present
        log(f"  HUC{huc}: building HAND + baseline SRC...")
        FU.build_hand_src(aoi, None)
    hts = list((wsd/"branches").glob("*/hydroTable_*.csv"))
    if not hts:
        raise RuntimeError(f"HUC{huc}: build produced NO per-branch hydroTables (SRC/crosswalk failed) -- rebuild needed")
    fic = aoi/"feature_id.csv"                                        # NWM discharge needs this; derive from hydroTables if absent
    if not fic.exists():
        fids = set()
        for h in hts: fids |= set(pd.read_csv(h, usecols=["feature_id"])["feature_id"].astype("int64").tolist())
        pd.DataFrame({"feature_id": sorted(fids)}).to_csv(fic, index=False)
        log(f"  HUC{huc}: wrote feature_id.csv ({len(fids)} ids)")
    return aoi

def ensure_subdivision(aoi):
    wsd = aoi/"watershed-data"; marker = wsd/"_subdiv.done"
    if marker.exists(): return
    for o in (wsd/"branches").glob("*/hydroTable_*.csv.orig"): o.unlink()   # drop stale pre-subdiv .orig
    FU.apply_subdivision(aoi, 0.06, 0.12)
    for ht in (wsd/"branches").glob("*/hydroTable_*.csv"):                  # snapshot subdivided baseline
        shutil.copy2(ht, ht.with_name(ht.name + ".orig"))
    marker.write_text("subdivided " + time.strftime("%Y-%m-%d %H:%M:%S"))

def swap_slope(aoi, slope_map):
    wsd = aoi/"watershed-data"
    for ht in sorted((wsd/"branches").glob("*/hydroTable_*.csv")):
        base = pd.read_csv(ht.with_name(ht.name + ".orig"))
        if slope_map:
            fids = base["feature_id"].astype("int64"); qc = base.columns.get_loc("discharge_cms"); sc = base.columns.get_loc("SLOPE")
            for fid, sn in slope_map.items():
                m = (fids == fid).values
                if not m.any(): continue
                so = base.loc[m, "SLOPE"].values; ok = (so > 0) & (sn > 0)
                if not ok.any(): continue
                idx = np.where(m)[0][ok]
                base.iloc[idx, qc] = base.iloc[idx, qc].values * np.sqrt(sn/so[ok])
                base.iloc[idx, sc] = sn
        base.to_csv(ht, index=False)
        ht.with_suffix(".parquet").unlink(missing_ok=True)
    (wsd/"hydrotable.parquet").unlink(missing_ok=True); (wsd/"hydrotable.csv").unlink(missing_ok=True)  # force per-branch use

def feature_ids(aoi, reach):
    streams = next((aoi/"watershed-data").glob("*_subset_streams.gpkg"), None)
    nwm = pyogrio.read_dataframe(streams, columns=["ID"]).to_crs(5070)
    g = pyogrio.read_dataframe(SWORD, where=f"reach_id={reach}").set_crs(4326, allow_override=True).to_crs(5070)
    rl = gpd.GeoDataFrame(geometry=[g.geometry.iloc[0]], crs=5070)
    j = gpd.sjoin_nearest(nwm, rl, distance_col="d", max_distance=1000.0)
    return set(int(x) for x in j.ID)

def gauge_discharge(reach, gq, bench):
    for fn, param in [(nwis.get_dv, "_Mean"), (nwis.get_iv, "")]:
        try:
            df, _ = fn(sites=gq, parameterCd=["00060"], start=bench, end=bench); df = df.reset_index()
            c = next((x for x in df.columns if x.startswith("00060") and (x.endswith(param) if param else not x.endswith("_cd"))), None)
            if c and len(df):
                v = pd.to_numeric(df[c], errors="coerce"); v = v.iloc[0] if param else v.mean()
                if v == v: return float(v)*CFS
        except Exception: pass
    return GAUGE_Q_FALLBACK.get(reach, float("nan"))

def run_fim(aoi, grp, all_fids):
    if grp["driver"] == "gauge":
        ddir = aoi/"discharge-inputs"; ddir.mkdir(exist_ok=True)
        rows = []
        for r in grp["reaches"]:
            q = gauge_discharge(r, grp["gq"][r], grp["bench"])
            rows += [{"feature_id": f, "discharge_cms": q} for f in sorted(all_fids[r])]
            log(f"    gauge-driven {r} Q={q:.0f} m3/s ({len(all_fids[r])} fids)")
        fq = ddir/f"gauge_{grp['bench']}.csv"; pd.DataFrame(rows).to_csv(fq, index=False)
        res = generateFIM(aoi, n_workers=NW, depth=True).from_discharge_inputs(csv=str(fq))
    else:
        day = pd.to_datetime(grp["bench"]).strftime("%Y-%m-%d"); vt = pd.to_datetime(grp["bench"]).strftime("%Y-%m-%d %H:00:00")
        getNWMretrospective(aoi, date=vt)
        res = generateFIM(aoi, n_workers=NW, depth=True).from_discharge_inputs(date=day)
    exts = [Path(getattr(r, "extent_path", "")) for r in (res or []) if getattr(r, "extent_path", None)]
    if exts: return exts[-1]
    tifs = sorted((aoi/"fim-outputs").glob("*inundation*.tif"), key=lambda p: p.stat().st_mtime)
    return tifs[-1] if tifs else None

def dest_path(aoi, grp, treat, reach=None):
    fo = aoi/"fim-outputs"
    if grp["driver"] == "gauge":                # gauge groups are single-reach here -> reach<r>_<t>_gaugedriven.tif
        return fo/f"reach{reach or grp['reaches'][0]}_{treat}_gaugedriven.tif"
    return fo/f"batch_{grp['huc']}_{grp['bench']}_{treat}.tif"

def main():
    log(f"fimbox {getattr(fimbox,'__version__','?')} | subdivision ON | calibration OFF | workers={NW}"
        + (f" | ONLY_REACH={ONLY}" if ONLY else ""))
    for huc, grp in GROUPS.items():
        grp = dict(grp, huc=huc)
        if ONLY and ONLY not in grp["reaches"]: continue
        try:
            aoi = stage_and_build(huc)
            ensure_subdivision(aoi)
            all_fids = {r: feature_ids(aoi, r) for r in grp["reaches"]}
        except Exception as e:
            log(f"HUC{huc}: SETUP ERROR {e}\n{traceback.format_exc()[-500:]}"); continue
        all_fids = {r: f for r, f in all_fids.items() if f}
        if not all_fids: log(f"HUC{huc}: no feature_ids, skip"); continue
        log(f"HUC{huc} {grp['bench']} {grp['driver']} reaches={list(all_fids)} fids={ {r: len(f) for r,f in all_fids.items()} }")
        for treat in TREATS:
            dest = dest_path(aoi, grp, treat)
            if dest.exists() and grp["driver"] != "gauge" and not FORCE: log(f"  {treat}: exists, skip"); continue
            # JOINT slope map: each reach's fids -> that reach's treatment slope (m/m)
            smap = {}
            for r, fids in all_fids.items():
                s = st.loc[r, SLOPE_COL[treat]] if r in st.index else np.nan
                if s == s and s > 0:
                    for f in fids: smap[f] = s/1e6
            if not smap: log(f"  {treat}: no slope, skip"); continue
            t0 = time.time()
            try:
                swap_slope(aoi, smap)
                ext = run_fim(aoi, grp, all_fids)
                if ext and Path(ext).exists():
                    for r in all_fids:                          # gauge groups: one tif per reach name
                        shutil.copy2(ext, dest_path(aoi, grp, treat, r))
                    log(f"  {treat}: OK {time.time()-t0:.0f}s -> {dest.name}")
                else:
                    log(f"  {treat}: no FIM extent ({time.time()-t0:.0f}s)")
            except Exception as e:
                log(f"  {treat}: ERROR {e}\n{traceback.format_exc()[-500:]}")
        swap_slope(aoi, {})                                     # restore subdivided baseline for the HUC
    log("REGEN DONE")

if __name__ == "__main__":
    main()
