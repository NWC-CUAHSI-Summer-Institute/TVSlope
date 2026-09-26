# Reach -> NWM feature_id resolution (RiverJoin-style) + AOI directory lookup.
from pathlib import Path
from types import SimpleNamespace
import geopandas as gpd, pyogrio
from final_config import DATA, SWORD
FIMBOX_OUT = DATA/"fimbox_out"; FIMBOX_OUT.mkdir(parents=True, exist_ok=True)
def _aoi_dir(huc8):
    huc8 = str(huc8).zfill(8)
    for c in [FIMBOX_OUT/f"HUC{huc8}"] + [p.parent for p in FIMBOX_OUT.glob(f"*{huc8}*/watershed-data")]:
        if (c/"watershed-data").is_dir(): return c
    return None
def reach_feature_ids(aoi_dir, reach_ids, tol_m=1000.0):
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
FR  = SimpleNamespace(SWORD=SWORD, FIMBOX_OUT=FIMBOX_OUT, _aoi_dir=_aoi_dir, reach_feature_ids=reach_feature_ids)


# ---- slope treatments: how each treatment assigns a slope to a reach --------  # sebastian update
# This is the provenance of data/slope_treatments.csv, which the notebooks previously only consumed.
# Ported from Sebastian Marshall's fim_reach.py; the gauge slope now goes through the datum-harmonised
# per_reach3.twin_series, so every gauge pair is on one vertical datum before it is differenced.
import numpy as _np
import pandas as pd
from per_reach3 import P3 as _P


def _fimhf_iris_table():
    """The COMBINED HFIRIS-SWORD slope (m/m) per SWORD reach_id (Chen 2025, `slope_iris_sword`).

    One combined hydrofabric+IRIS+SWORD product, NOT separate hydrofabric / IRIS / SWORD slopes.
    FIMHF_IRIS_new.csv carries the newest values (~1.6k reaches); FIMHF_IRIS_v1.0.csv fills the rest
    (~117k reaches) so nearly every study reach has a baseline.
    """
    def _load(fn):
        d = pd.read_csv(DATA/fn, usecols=["reach_id", "slope_iris_sword"], low_memory=False)
        d["reach_id"] = d.reach_id.astype("float").astype("int64").astype(str)
        return d.drop_duplicates("reach_id").set_index("reach_id")["slope_iris_sword"]
    return _load("FIMHF_IRIS_new.csv").combine_first(_load("FIMHF_IRIS_v1.0.csv"))


def iris_sword_new_slope(reach_id):
    """slope-HFIRIS-SWORD: the combined hydrofabric+IRIS+SWORD static slope (m/m) for this reach."""
    t = _fimhf_iris_table(); rid = str(reach_id)
    v = float(t[rid]) if rid in t.index else _np.nan
    return v if v == v and v > 0 else _np.nan


def swot_median_slope(reach_id):
    """slope-SWOT-median: the reach's median SWOT water-surface slope (m/m), QC'd and sign-corrected."""
    s = _P.swot_clean(str(reach_id))
    return float(s.slope_c.median()) if len(s) else _np.nan


def swot_floodstage_slope(reach_id, q=0.90):
    """slope-SWOT-floodstage: the slope OBSERVED on the overpass nearest flood stage.

    Flood stage is the P90 of the per-pass SWOT stage H = WSE - min(WSE), i.e. the reach's own
    low-water datum. The slope is not modelled or extrapolated: it is the measured slope of the ACTUAL
    pass closest to that stage. So it is less noisy than the single WSE-maximum pass
    (slope-SWOT-maxWSE) yet still a genuine high-flow measurement rather than the whole-record median.
    Falls back to the median when there are too few clean passes (< 8) to define a stage distribution.
    """
    s = _P.swot_clean(str(reach_id))
    s = s.dropna(subset=["wse", "slope_c"]) if len(s) else s
    s = s[s.slope_c > 0] if len(s) else s
    if len(s) < 8: return swot_median_slope(reach_id)
    stage = s.wse - s.wse.min()
    h_flood = float(stage.quantile(q))
    idx = (stage - h_flood).abs().idxmin()
    v = float(s.loc[idx, "slope_c"])
    return v if v == v and v > 0 else swot_median_slope(reach_id)


def swot_maxwse_slope(reach_id):
    """slope-SWOT-maxWSE: the water-surface slope of the single largest-WSE overpass (m/m)."""
    s = _P.swot_clean(str(reach_id))
    s = s.dropna(subset=["wse", "slope_c"]) if len(s) else s
    if not len(s): return _np.nan
    return float(s.loc[s.wse.idxmax(), "slope_c"])


def gauge_slope(row, kind="median"):
    """slope-gauge: the twin-gauge water-surface slope (m/m) from S(t) = (WSE_up - WSE_dn) / span.

    kind='median' -> median of the daily series.
    kind='maxwse' -> flood-stage slope: the median slope over the top-decile upstream-WSE days.

    Both gauges are on one vertical datum here, because per_reach3.wse_series harmonises alt_va onto
    datum.GAUGE_REF_DATUM first. Differencing a NGVD29 gauge against a NAVD88 one puts the datum
    offset straight into the slope.
    """
    tw = _P.twin_series(row)
    if not len(tw): return _np.nan
    S = tw.S.dropna()
    if not len(S): return _np.nan
    if kind == "maxwse" and "wu" in tw and tw.wu.notna().any():
        hi = tw[(tw.wu >= tw.wu.quantile(0.9)) & tw.S.notna()]
        if len(hi): return float(hi.S.median())
    return float(S.median())


_SLOPE_FN = {"hfirissword_new": lambda row: iris_sword_new_slope(str(row.reach)),
             "swot_median":     lambda row: swot_median_slope(str(row.reach)),
             "swot_floodstage": lambda row: swot_floodstage_slope(str(row.reach)),
             "swot_maxwse":     lambda row: swot_maxwse_slope(str(row.reach)),
             "gauge_median":    lambda row: gauge_slope(row, "median"),
             "gauge_maxwse":    lambda row: gauge_slope(row, "maxwse")}

TREATMENTS = [("slope-HFIRIS-SWORD(new)", "hfirissword_new"),   # IRIS v3.3 + hydrofabric + SWORD v17b
              ("slope-SWOT-median",       "swot_median"),
              ("slope-SWOT-floodstage",   "swot_floodstage"),   # SWOT slope at flood (P90 WSE) stage
              ("slope-SWOT-maxWSE",       "swot_maxwse"),       # per-pass SRC at the largest-WSE overpass
              ("slope-gauge-median",      "gauge_median")]      # median twin-gauge slope


def treatment_slopes(row):
    """The slope (m/m) each treatment assigns to one reach row -- the comparison table's own source."""
    return {lab: _SLOPE_FN[key](row) for lab, key in TREATMENTS}


FR.treatment_slopes = treatment_slopes          # expose on the namespace the notebooks already import
FR.TREATMENTS = TREATMENTS
