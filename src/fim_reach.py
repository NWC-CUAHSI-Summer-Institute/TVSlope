"""Reach-keyed FIMbox flood-inundation-map generator for work6 (calibration CLOSED).

Ported from the FIMbox engine in work4-3.ipynb §9/§10 (the fimserve/FIMBench evaluation machinery is
intentionally NOT ported — this only *makes* the FIM). Given a study reach it, end to end:

    1. resolves the reach's HUC8 (NWIS huc_cd of the on-reach discharge gauge),
    2. stages DEM/NWM/gages for the HUC once  (fimbox.getAllInputData, cached),
    3. builds HAND + an uncalibrated synthetic rating curve once per HUC (cached; run_calibration NEVER
       called, so the injected slope is the ONLY SRC modification),
    4. injects the "new src" = the reach's SWOT median water-surface slope into that reach's NWM
       feature_id(s) via the exact Manning rescale  Q *= sqrt(S_new/S_old)  (fimbox_swap_slope),
    5. runs generateFIM for a high-flow event date and returns the inundation-extent raster,
    6. plots the extent on an Esri satellite basemap with the SWOT reach + gauges.

feature_id <-> reach is resolved GEOMETRICALLY (RiverJoin-lite): the SWORD reach centerline is matched to
the nearest NWM flowline(s) in <AOI>/watershed-data/baseline_subset_streams.gpkg (its `ID` == hydroTable
`feature_id`). No dependency on work4-3's `final`/RiverJoin table.

Run with the fimserve conda kernel (has fimbox). Heavy steps (stage/HAND) are cached under data/fimbox_out/.
"""
import warnings; warnings.filterwarnings("ignore")
import os; os.environ.pop("PROJ_DATA", None); os.environ.pop("PROJ_LIB", None)
import glob, shutil
from pathlib import Path
import numpy as np, pandas as pd
import geopandas as gpd, pyogrio
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import ListedColormap
from scipy.stats import theilslopes
import functools

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


ROOT = _resolve_root(); DATA = ROOT/"data"
SWORD = DATA/"SWORD_v17b_gpkg"/"na_sword_reaches_v17b.gpkg"
FIMBOX_OUT = DATA/"fimbox_out"; FIMBOX_OUT.mkdir(parents=True, exist_ok=True)
DIS = DATA/"discharge"; CFS = 0.028316846592
FEAT, SLOPE_COL, Q_COL = "feature_id", "SLOPE", "discharge_cms"
UPC, MIDC, DNC = "#1f77b4", "#e53935", "#2ca02c"
try: import contextily as cx; HAVE_CX = True
except Exception: HAVE_CX = False

import find_reaches3 as _F              # gauge_huc8 (cached), _discharge
import per_reach3 as _P                 # swot_clean (QC + sign correction), GC gauge coords

# ---- fimbox (import lazily-friendly) ----
import fimbox
from fimbox._dask import _resolve_n_workers
_NW = _resolve_n_workers()


# ---- PATCH: 3DEP DEM staging SEGFAULTS on macOS because fimbox fetches tiles in a ThreadPoolExecutor and
# GDAL/rasterio inside py3dep is not thread-safe here (single-threaded py3dep.get_dem works fine). Replace the
# threaded fetch with a main-thread SERIAL loop so new HUCs can be staged/built (fixes the "Segmentation fault:
# 11 during --- DEM (3DEP) ---" crash). Same output (tiles merged in WGS84), just no worker threads. ----
import sys as _sys, subprocess as _subprocess
_THIS_DIR = Path(__file__).resolve().parent

def _dem_run_patched(self):
    """Replacement for DEMProcessor.run(): fetch the 3DEP DEM in a CLEAN SUBPROCESS (code/fetch_dem_worker.py,
    which imports NO pyogrio) and write the final GeoTIFF. Root cause: fimbox reads boundaries with pyogrio,
    which corrupts the shared GDAL/PROJ global state, so the in-process py3dep.get_dem (rasterio, remote COG)
    SEGFAULTS on macOS. Isolating the fetch in a fresh process gives it clean GDAL state. Output path +
    skip-if-valid mirror the original run(); local-DEM path and merge conditioning are left to the worker."""
    from fimbox._skip_if_valid import should_skip
    from shapely import wkt as _wkt
    save_path = self.output_dir / (self.out_name or ("processed_local_dem.tif" if self.dem_file
                                   else f"3dep_dem_{self.resolution}m.tif"))
    if should_skip(save_path):
        self.logger.info(f"DEM output already valid, skipping: {save_path}"); return str(save_path)
    if self.dem_file:
        return _DEM_RUN_ORIG(self)                        # local DEM file: keep original behaviour
    wkt_file = self.output_dir / "_dem_boundary.wkt"
    wkt_file.write_text(_wkt.dumps(self.boundary_geom))   # WGS84 boundary, written without GDAL/pyogrio
    self.logger.info(f"Fetching 3DEP DEM in a CLEAN SUBPROCESS (pyogrio/rasterio GDAL-conflict fix) -> {save_path}")
    r = _subprocess.run([_sys.executable, str(_THIS_DIR/"fetch_dem_worker.py"), str(wkt_file),
                         str(self.target_crs), str(self.resolution), str(save_path), "0.2"],
                        capture_output=True, text=True)
    if not save_path.exists():
        raise RuntimeError(f"3DEP subprocess DEM fetch failed.\n{(r.stdout or '')[-500:]}{(r.stderr or '')[-300:]}")
    self.logger.info(f"DEM saved to {save_path} (subprocess)"); return str(save_path)

try:
    from fimbox.preprocessing.download_data.dem_process import DEMProcessor as _DEMP
    _DEM_RUN_ORIG = _DEMP.run
    _DEMP.run = _dem_run_patched
    _DEMP.max_workers = 1
except Exception as _e:
    print(f"[fim_reach] DEM subprocess patch not applied: {_e}")


# ===================================================================== slope / feature-id helpers
def swot_median_slope(reach_id):
    """Reach's SWOT median water-surface slope (m/m), QC-cleaned + sign-corrected (per_reach3.swot_clean)."""
    s = _P.swot_clean(str(reach_id))
    return float(s.slope_c.median()) if len(s) else np.nan


def gauge_slope(row, kind="median"):
    """GAUGE (twin-gauge) water-surface slope (m/m) from the up/down WSE series S(t)=(WSE_up-WSE_dn)/span.
    kind='median' -> median of the daily series; kind='maxwse' -> the flood-stage slope = median slope over
    the top-decile upstream-WSE days (the slope that holds when the water surface is highest)."""
    tw = _P.twin_series(row)                 # per_reach3.twin_series uses _span_m(row) (span_m or span_km*1000)
    if not len(tw): return np.nan
    S = tw.S.dropna()
    if not len(S): return np.nan
    if kind == "maxwse" and "wu" in tw and tw.wu.notna().any():
        hi = tw[(tw.wu >= tw.wu.quantile(0.9)) & tw.S.notna()]
        if len(hi): return float(hi.S.median())
    return float(S.median())


@functools.lru_cache(maxsize=1)
def _fimhf_iris_table():
    """The COMBINED HFIRIS-SWORD slope (m/m) per SWORD reach_id — a single combined hydrofabric+IRIS+SWORD
    product (Chen 2025; column `slope_iris_sword`), NOT separate hydrofabric / IRIS / SWORD slopes. Uses
    FIMHF_IRIS_new.csv (the newest values, ~1.6k reaches) with FIMHF_IRIS_v1.0.csv as a fallback for coverage
    (~117k reaches) so nearly every study reach has a HFIRIS-SWORD baseline."""
    def _load(fn):
        d = pd.read_csv(DATA/fn, usecols=["reach_id", "slope_iris_sword"], low_memory=False)
        d["reach_id"] = d.reach_id.astype("float").astype("int64").astype(str)
        return d.drop_duplicates("reach_id").set_index("reach_id")["slope_iris_sword"]
    new, full = _load("FIMHF_IRIS_new.csv"), _load("FIMHF_IRIS_v1.0.csv")
    return new.combine_first(full)          # new takes priority; v1.0 fills the rest


def iris_sword_new_slope(reach_id):
    """slope-HFIRIS-SWORD: the COMBINED hydrofabric+IRIS+SWORD slope (m/m) for this reach, read directly from
    data/FIMHF_IRIS_new.csv (slope_iris_sword). One combined product per reach — we do not separately consider
    hydrofabric / IRIS / SWORD slopes."""
    t = _fimhf_iris_table(); rid = str(reach_id)
    v = float(t[rid]) if rid in t.index else np.nan
    return v if v == v and v > 0 else np.nan


def swot_floodstage_slope(reach_id, q=0.90):
    """slope-SWOT-floodstage: the water-surface slope OBSERVED on the SWOT overpass at flood stage, where
    flood stage is the P90 of the per-pass SWOT stage  H = WSE - min(WSE)  (i.e. the reach's own low-water
    datum, matching the project's Stage = WSE - historical-min-WSE definition, 01_project_outline.md).

    We do NOT model/extrapolate the slope: we take the ACTUAL pass whose stage is closest to the P90 stage,
    and return that pass's measured slope. This is a real, single-overpass observation at a robust high-flow
    level (P90), so it is (a) less noisy than the single WSE-maximum pass [slope-SWOT-maxWSE], yet (b) still a
    genuine flood-stage measurement rather than the whole-record median [slope-SWOT-median]. Falls back to the
    median only when there are too few clean passes to define a stage distribution (< 8)."""
    s = _P.swot_clean(str(reach_id))
    s = s.dropna(subset=["wse", "slope_c"]) if len(s) else s
    s = s[s.slope_c > 0] if len(s) else s
    if len(s) < 8: return swot_median_slope(reach_id)
    stage = s.wse - s.wse.min()                       # per-pass stage above the reach's SWOT low-water datum
    h_flood = float(stage.quantile(q))                # P90 flood stage
    idx = (stage - h_flood).abs().idxmin()            # the ACTUAL overpass nearest the P90 stage
    v = float(s.loc[idx, "slope_c"])
    return v if v == v and v > 0 else swot_median_slope(reach_id)


def swot_maxwse_slope(reach_id):
    """slope-SWOT-maxWSE: per SWOT overpass we get an SRC (its own slope); pick the SRC from the pass
    with the LARGEST SWOT WSE -> that single extreme pass's water-surface slope (m/m). Contrast with
    slope-SWOT-floodstage, which uses the more robust P90-stage pass instead of the single maximum."""
    s = _P.swot_clean(str(reach_id))
    s = s.dropna(subset=["wse", "slope_c"]) if len(s) else s
    if not len(s): return np.nan
    return float(s.loc[s.wse.idxmax(), "slope_c"])


# ---- the 5 slope treatments for work6 (as in work4-3), compared against the uncalibrated baseline SRC ----
_SLOPE_FN = {"hfirissword_new": lambda row: iris_sword_new_slope(str(row.reach)),
             "swot_median":     lambda row: swot_median_slope(str(row.reach)),
             "swot_floodstage": lambda row: swot_floodstage_slope(str(row.reach)),
             "swot_maxwse":     lambda row: swot_maxwse_slope(str(row.reach)),
             "gauge_median":    lambda row: gauge_slope(row, "median"),
             "gauge_maxwse":    lambda row: gauge_slope(row, "maxwse"),
             "swot":            lambda row: swot_median_slope(str(row.reach))}

TREATMENTS = [("slope-HFIRIS-SWORD(new)", "hfirissword_new"),   # IRIS v3.3 + hydrofabric + SWORD v17b
              ("slope-SWOT-median",       "swot_median"),
              ("slope-SWOT-floodstage",   "swot_floodstage"),   # SWOT slope at flood (P90 WSE) stage
              ("slope-SWOT-maxWSE",       "swot_maxwse"),       # per-pass SRC at the largest-WSE overpass (NEW)
              ("slope-gauge-median",      "gauge_median")]       # median twin-gauge slope

def treatment_slopes(row):
    "slope (m/m) each of the 5 treatments assigns to a reach row (for a comparison table)."
    return {lab: _SLOPE_FN[key](row) for lab, key in TREATMENTS}


def reach_feature_ids(aoi_dir, reach_ids, tol_m=1000.0):
    """NWM feature_id(s) whose flowline is within tol_m of any given SWORD reach centerline.
    Returns a set of ints (== hydroTable feature_id). reach_ids: one id or an iterable."""
    if isinstance(reach_ids, (str, int)): reach_ids = [reach_ids]
    streams = Path(aoi_dir)/"watershed-data"/"baseline_subset_streams.gpkg"
    if not streams.exists():
        streams = next((Path(aoi_dir)/"watershed-data").glob("*_subset_streams.gpkg"), None)
    if streams is None: return set()
    nwm = pyogrio.read_dataframe(streams, columns=["ID"]).to_crs(5070)
    lines = []
    for r in reach_ids:
        try:
            gg = pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(r)}")
            if len(gg): lines.append(gg.set_crs(4326, allow_override=True).to_crs(5070).geometry.iloc[0])
        except Exception: pass
    if not lines: return set()
    rl = gpd.GeoDataFrame(geometry=lines, crs=5070)
    j = gpd.sjoin_nearest(nwm, rl, distance_col="d", max_distance=tol_m)
    return set(j.ID.astype("int64").tolist())


def _inject_hydrotable_df(ht, slope_map):
    """SLOPE := S_new and discharge_cms *= sqrt(S_new/S_old) for every feature_id in slope_map.
    The uncalibrated SRC is pure Manning (Q ~ sqrt(SLOPE)), so this equals rebuilding the SRC at S_new."""
    ht = ht.copy(); fids = ht[FEAT].astype("int64")
    qcol = ht.columns.get_loc(Q_COL); scol = ht.columns.get_loc(SLOPE_COL); changed = 0
    for fid, s_new in slope_map.items():
        mask = (fids == fid).values
        if not mask.any(): continue
        s_old = ht.loc[mask, SLOPE_COL].values; sn = np.full(mask.sum(), float(s_new))
        ok = (s_old > 0) & (sn > 0)
        if not ok.any(): continue
        idx = np.where(mask)[0][ok]
        ht.iloc[idx, qcol] = ht.iloc[idx, qcol].values * np.sqrt(sn[ok]/s_old[ok])
        ht.iloc[idx, scol] = sn[ok]; changed += int(ok.sum())
    return ht, changed


# ===================================================================== fimbox stage / build / run
def _aoi_dir(huc8):
    huc8 = str(huc8).zfill(8)
    for c in [FIMBOX_OUT/f"HUC{huc8}"] + [p.parent for p in FIMBOX_OUT.glob(f"*{huc8}*/watershed-data")]:
        if (c/"watershed-data").is_dir(): return c
    return None


def _fully_staged(aoi):
    "True only if the streams file exists (a partial folder with just DEM/WBD is NOT fully staged)."
    return aoi is not None and bool(list((Path(aoi)/"watershed-data").glob("*_subset_streams.gpkg")))


def stage(huc8):
    """Download DEM/NWM/gages for the HUC once (cached). Returns the AOI working dir. Re-runs getAllInputData
    when the folder is only PARTIAL (e.g. DEM staged but flowlines/catchments missing) — getAllInputData
    skips the already-valid DEM, so this just completes the missing streams/catchments."""
    huc8 = str(huc8).zfill(8)
    aoi = _aoi_dir(huc8)
    if _fully_staged(aoi): return aoi
    fimbox.getAllInputData(huc8=huc8, out_dir=str(FIMBOX_OUT), buffer_m=2000, headwater_buffer_cells=8,
                           get_flowlines=True, get_catchments=True, resolution="medium", identifier="nwm").run()
    return _aoi_dir(huc8)


def build_hand_once(aoi_dir):
    """BranchDerivation + HAND/SRC for every branch — the HEAVY step, ONCE per HUC (cached when branch
    hydroTables already exist). Slope here is a placeholder swapped per-reach later. NO calibration."""
    wsd = Path(aoi_dir)/"watershed-data"
    if list((wsd/"branches").glob("*/hydroTable_*.csv")): return False
    ident = next(wsd.glob("*_subset_streams.gpkg")).name.split("_subset_streams")[0]
    fimbox.BranchDerivation(out_dir=wsd, branch_id_attribute="levpa_id", reach_id_attribute="ID",
                            branch_buffer_distance_meters=7000.0).run()
    _opt = lambda p: p if p.exists() else None
    cfg = fimbox.AOIProcessingConfig(
        aoi_dir=wsd, branch_list_path=wsd/"branch_ids.lst", dem_path=wsd/"dem.tif",
        streams_gpkg=wsd/f"{ident}_subset_streams.gpkg", boundary_gpkg=wsd/"wbd_buffered.gpkg",
        bridge_elev_diff_path=_opt(wsd/"bridge_elev_diff.tif"),
        levee_gpkg_path=_opt(wsd/"3d_nld_subset_levees_burned.gpkg"),
        headwaters_gpkg=_opt(wsd/f"{ident}_headwaters.gpkg"),
        levelpaths_extended_gpkg=_opt(wsd/f"{ident}_subset_streams_levelPaths_extended.gpkg"),
        mannings_n=0.06, stage_min_m=0.0, stage_interval_m=0.3048, stage_max_m=25.2984,
        min_catchment_area=0.25, min_stream_length=0.5, crosswalk_max_distance_m=100.0,
        src_slope_source="iris_sword", iris_slope_csv=None,
        n_workers=_NW, keep_failed_branches=True, delete_deny_list=True)
    fimbox.calculate_allbranches(cfg, run_branch_zero=True, branch_ids_csv=wsd/"branch_ids.csv")
    return True


def swap_slope(aoi_dir, slope_map):
    """Inject slope into every branch hydroTable by the exact Manning rescale (restores from a one-time
    .orig baseline so treatments don't compound). slope_map={feature_id: m/m}; empty -> baseline restored."""
    wsd = Path(aoi_dir)/"watershed-data"; n = 0
    for ht in sorted((wsd/"branches").glob("*/hydroTable_*.csv")):
        orig = ht.with_name(ht.name + ".orig")
        if not orig.exists(): shutil.copy2(ht, orig)
        base = pd.read_csv(orig)
        if slope_map: base, _ = _inject_hydrotable_df(base, slope_map)
        base.to_csv(ht, index=False)
        ht.with_suffix(".parquet").unlink(missing_ok=True)   # generateFIM prefers parquet -> drop stale
        n += 1
    return n


def _run_fim(aoi_dir, event_date):
    """NWM retrospective discharge for the event -> generateFIM -> newest inundation-extent raster."""
    aoi_dir = Path(aoi_dir)
    day = pd.to_datetime(event_date).strftime("%Y-%m-%d")
    vt = pd.to_datetime(event_date).strftime("%Y-%m-%d %H:00:00")
    fimbox.getNWMretrospective(aoi_dir, date=vt)
    res = fimbox.generateFIM(aoi_dir, n_workers=_NW, depth=True).from_discharge_inputs(date=day)
    exts = [getattr(r, "extent_path", None) for r in (res or [])]
    exts = [Path(e) for e in exts if e]
    if exts: return exts[-1]
    tifs = sorted((aoi_dir/"fim-outputs").glob("*inundation*.tif"), key=lambda p: p.stat().st_mtime)
    return tifs[-1] if tifs else None


# ===================================================================== event date
def peak_event_date(gq, lo="2010-01-01", hi="2022-12-31"):
    """Highest-discharge day within the NWM-retrospective window for the gauge (for a representative flood).
    Falls back to a fixed date if the gauge has no cached discharge."""
    try:
        d = _F._discharge(gq)
        if len(d):
            d = d.dropna(subset=["discharge_cms"])
            d = d[(d.datetime >= lo) & (d.datetime <= hi)]
            if len(d): return pd.to_datetime(d.loc[d.discharge_cms.idxmax(), "datetime"]).strftime("%Y-%m-%d")
    except Exception: pass
    return "2019-05-01"


# ===================================================================== top-level: FIM for a reach
def generate_fim_for_reach(row, event_date=None, inject="gauge_median", extra_reaches=None, tag=None, verbose=True):
    """Full pipeline for one study-reach row (needs .reach, .gq, and .huc8 — else HUC8 is resolved from gq).
    inject (the "new src"): 'gauge_median' (default) -> median twin-gauge slope; 'gauge_maxwse' -> flood-stage
    twin-gauge slope; 'swot' -> SWOT median slope; 'baseline'/None -> uninjected SRC; or a float (m/m). The
    extent raster is copied to a (reach, treatment)-tagged filename so baseline and new-src runs don't clobber
    each other. Returns dict(reach, huc8, aoi_dir, event_date, slope_new, feature_ids, extent_tif)."""
    reach = str(row.reach); gq = str(getattr(row, "gq", "") or getattr(row, "gmid", ""))
    huc8 = str(getattr(row, "huc8", "") or "").zfill(8)
    if not huc8 or huc8 == "00000000" or not huc8.isdigit():
        huc8 = _F.gauge_huc8(gq)
    if not huc8 or not str(huc8).isdigit():
        return dict(reach=reach, huc8=huc8, error="no HUC8")
    huc8 = str(huc8).zfill(8)
    if verbose: print(f"[{reach}] HUC {huc8} · gauge {gq}")
    aoi = stage(huc8)
    if aoi is None: return dict(reach=reach, huc8=huc8, error="staging failed")
    built = build_hand_once(aoi)
    if verbose: print(f"  HAND {'built' if built else 'cached'} at {aoi}")
    fids = reach_feature_ids(aoi, [reach] + list(extra_reaches or []))
    if inject in (None, "baseline"):
        slope_map = {}; s_new = np.nan
    else:
        s_new = _SLOPE_FN[inject](row) if inject in _SLOPE_FN else float(inject)
        if not (s_new == s_new): return dict(reach=reach, huc8=huc8, error=f"no {inject} slope")
        slope_map = {f: s_new for f in fids}
    swap_slope(aoi, slope_map)
    if verbose: print(f"  injected {'baseline (none)' if not slope_map else f'{len(slope_map)} feature_id(s) @ {s_new*1e6:.0f} mm/km ({inject})'}")
    ed = event_date or peak_event_date(gq)
    if verbose: print(f"  event {ed} -> generateFIM ...")
    ext = _run_fim(aoi, ed)
    if ext:                                              # snapshot to a (reach, treatment)-tagged file
        tg = tag or ("baseline" if not slope_map else (inject if isinstance(inject, str) else "inject"))
        dest = Path(aoi)/"fim-outputs"/f"reach{reach}_{tg}_inundation.tif"
        shutil.copy2(ext, dest); ext = dest
    return dict(reach=reach, huc8=huc8, aoi_dir=str(aoi), event_date=ed, slope_new=s_new,
                slope_kind=(inject if isinstance(inject, str) else "inject"),
                feature_ids=sorted(fids), extent_tif=(str(ext) if ext else None))


# ===================================================================== plotting
def plot_fim(result, row=None, ax=None, title=None, zoom_pad=0.35, save=None):
    """Plot the inundation extent on an Esri satellite basemap with the SWOT reach + its gauges."""
    import rasterio
    from rasterio.warp import transform_bounds
    tif = result.get("extent_tif")
    if not tif or not Path(tif).exists():
        print("  no extent raster to plot"); return None
    own = ax is None
    if own: fig, ax = plt.subplots(figsize=(8.5, 8.8))
    with rasterio.open(tif) as ds:
        arr = ds.read(1); nod = ds.nodata
        wet = np.isfinite(arr) & (arr != (nod if nod is not None else -9999)) & (arr > 0)
        # extent in web-mercator
        b = ds.bounds; left, bottom, right, top = transform_bounds(ds.crs, "EPSG:3857", b.left, b.bottom, b.right, b.top)
    ax.imshow(np.where(wet, 1, np.nan), extent=[left, right, bottom, top], origin="upper",
              cmap=ListedColormap(["#1e63d8"]), alpha=0.62, zorder=3, interpolation="nearest")
    reach = str(result["reach"]); xs = []; ys = []
    try:
        rl = pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(reach)}").set_crs(4326, allow_override=True).to_crs(3857)
        rl.plot(ax=ax, color="#00e5ff", lw=2.6, zorder=4)
        b = rl.total_bounds; xs += [b[0], b[2]]; ys += [b[1], b[3]]
    except Exception: pass
    if row is not None:
        pts = [("upstream", getattr(row, "gup", None), UPC), ("on-reach", getattr(row, "gq", getattr(row, "gmid", None)), MIDC),
               ("downstream", getattr(row, "gdn", None), DNC)]
        for lab, g, col in pts:
            g = str(g) if g is not None and g == g else None
            if not g or g == "nan" or g not in _P.GC.index: continue
            p = gpd.GeoSeries([__import__("shapely").geometry.Point(float(_P.GC.loc[g, "gage_longitude"]),
                              float(_P.GC.loc[g, "gage_latitude"]))], crs=4326).to_crs(3857).iloc[0]
            ax.scatter(p.x, p.y, s=150, marker="^", color=col, ec="white", lw=1.4, zorder=6)
            ax.annotate(f"{lab}\n{g}", (p.x, p.y), color="white", fontsize=8, fontweight="bold",
                        xytext=(6, 4), textcoords="offset points", zorder=7)
            xs.append(p.x); ys.append(p.y)
    # frame to the study reach + its gauges (so the reach-scale FIM change is visible), else whole extent
    if xs and ys:
        cx0, cy0 = (min(xs)+max(xs))/2, (min(ys)+max(ys))/2
        half = max(max(xs)-min(xs), max(ys)-min(ys))/2*(1+zoom_pad*2) + 1500
        ax.set_xlim(cx0-half, cx0+half); ax.set_ylim(cy0-half, cy0+half)
    else:
        ax.set_xlim(left, right); ax.set_ylim(bottom, top)
    ax.set_xticks([]); ax.set_yticks([])
    if HAVE_CX:
        try: cx.add_basemap(ax, source=cx.providers.Esri.WorldImagery, crs="EPSG:3857", attribution_size=5)
        except Exception: pass
    riv = getattr(row, "river", "") if row is not None else ""
    smm = result.get("slope_new"); _lab = {"hfirissword_new": "HFIRIS-SWORD(new)", "swot_median": "SWOT median",
            "swot_floodstage": "SWOT flood-stage", "swot_maxwse": "SWOT max-WSE pass", "gauge_median": "median gauge",
            "gauge_maxwse": "max-WSE gauge", "swot": "SWOT slope"}.get(result.get("slope_kind"), "new-src")
    stag = f"new src: {_lab} slope {smm*1e6:.0f} mm/km" if smm and smm == smm else "baseline SRC"
    ax.set_title(title or f"{riv} — {reach}\nFIMbox flood extent ({stag}, event {result.get('event_date','?')})",
                 fontsize=11, fontweight="bold")
    ax.legend(handles=[Line2D([], [], color="#1e63d8", lw=6, alpha=.6, label="FIMbox inundation"),
                       Line2D([], [], color="#00e5ff", lw=3, label="SWOT reach"),
                       Line2D([], [], marker="^", color="w", mfc=MIDC, mec="white", ms=11, label="on-reach gauge")],
              loc="upper left", fontsize=8, framealpha=.85)
    if save: plt.savefig(save, dpi=130, bbox_inches="tight")
    if own: plt.show()
    return ax
