"""The causal footprint of a slope treatment, and the invariant that follows from it.

WHY THIS EXISTS. Jamshidi (2026-07-09, "River Mask for metric calculation") argues that the FIMBench
benchmark is a multi-source product: it carries lakes, reservoirs, tributaries and urban flooding that a
reach-scale slope change can never move. Scoring the whole scene therefore SUPPRESSES the slope signal in
the ratio. He is right, and the effect is large: for Neuse reach 73216000121 the catchments of the injected
HydroIDs cover 52.3 km2, while the evaluation box this study has been scoring covers about 144 km2. Roughly
two thirds of the scored area is INERT, so every CSI is diluted by a constant and the differences between
treatments are compressed toward zero.

WHERE THIS DIFFERS FROM THE MEMO. The memo wavers between two masks: "the branch the reach belongs to"
(step b) and "catchments belonging to the reach" (step c), and says "not 100% sure". They are not the same
thing. A branch is a whole level path, so masking to it re-imports catchments the injection never touched.
The defensible mask is (c), stated exactly: the union of the catchments of the HydroIDs the injector
actually modified. That is the only ground on which the treatment can act, it is derivable rather than
case-by-case, and it dissolves the memo's "challenges left" about an untouched tributary: an uninjected
tributary simply is not in the mask.

WHAT THE MASK ALSO BUYS: A CORRECTNESS TEST. If the flood map changes OUTSIDE the causal footprint, the
injection touched something it should not have. That is not a metric, it is an invariant, and it is not
hypothetical: this pipeline shipped a bug where HydroIDs (which HAND numbers PER BRANCH, so the same
integer names a different river in another branch) were used as the injection key, and 52% of the rescaled
rows landed on unrelated rivers. `outside_change` below would have failed that run on the first reach.

WHAT THE MASK COSTS. Masking changes what CSI MEANS. It becomes "skill where the slope can act", not
"flood-map accuracy", so it cannot be compared with published basin-wide HAND-FIM numbers, and a gain on
this domain must never be reported as a basin-scale improvement. Both numbers are therefore computed and
both are reported.

NOT ADOPTED: the memo's "keep only the largest flooded area" clean-up. HAND is a channel-connected model
and structurally cannot wet disconnected floodplain water, so dropping disconnected benchmark water removes
precisely the false-negative class HAND is worst at, and inflates CSI for every treatment. It may leave the
DIFFERENCE between treatments intact, but that is an assumption, not a result; it is left as a disclosed
sensitivity test rather than silently applied.

Author: Sebastian R.O. Marshall
"""
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask

EA = 5070                       # CONUS Albers equal-area: areas below are real areas
_CACHE = {}


def _hand_dir(root_run, huc):
    return os.path.join(root_run, "output", "flood_%s" % huc, huc)


def treated_rows(root_run, huc, hids, feats=None):
    """(HydroIDs, feature_ids) the injector really modifies.

    `feats` MUST be the crosswalk's own feature_ids, the same set inject() uses. Deriving them here from
    branch-0 rows (which is what this did) re-imports the per-branch HydroID collision, and then the MASK
    covers a different set of rivers than the INJECTION does. The consequence is not subtle: legitimate,
    correct changes inside the reach land outside the mask, and the causal-footprint invariant fires a false
    alarm. Measured on Caloosahatchee 73257400023, the mismatch reported 36,219 "outside" pixels on a run
    whose injection was in fact perfectly confined.
    """
    ht = pd.read_csv(os.path.join(_hand_dir(root_run, huc), "hydrotable.csv"),
                     usecols=["HydroID", "branch_id", "feature_id"], low_memory=False).drop_duplicates()
    tgt = ht[ht.HydroID.astype("int64").isin(set(int(h) for h in hids))]
    if feats is None:
        raise SystemExit("reach_mask needs the crosswalk's feature_ids. Deriving them from branch-0 rows "
                         "makes the mask disagree with the injection and the invariant fires falsely.")
    feats = set(int(f) for f in feats)
    hid_true = set(tgt[tgt.feature_id.astype("int64").isin(feats)].HydroID.astype("int64"))
    return hid_true, feats


def footprint(root_run, huc, hids, feats=None):
    """The union of the catchments of the treated reach, across EVERY branch, in EPSG:5070.

    ACROSS EVERY BRANCH, not just branch 0. HAND-FIM mosaics the inundation of all branches, and each branch
    carries its OWN catchment polygons (gw_catchments_..._crosswalked_<branch>.gpkg) with its own HydroID
    numbering. A footprint built from branch 0 alone is incomplete: the reach's level-path catchments are
    missing from it, so genuine, correct changes inside those catchments get counted as "outside the mask"
    and the invariant fires a false alarm. Measured: the branch-0-only mask gave the Ouachita a 4.4 km2
    footprint and flagged 29,059 "outside" pixels that were in fact inside the reach's own level-path
    catchments.

    Selection is by feature_id (the NWM reach id), which IS globally unique, rather than by HydroID, which
    HAND numbers per branch and which therefore collides across branches.
    """
    import glob
    key = (huc, tuple(sorted(int(h) for h in hids)))
    if key in _CACHE:
        return _CACHE[key]
    _, feats = treated_rows(root_run, huc, hids, feats)
    parts = []
    for gpkg in glob.glob(os.path.join(_hand_dir(root_run, huc), "branches", "*",
                                       "gw_catchments_reaches_filtered_addedAttributes_crosswalked_*.gpkg")):
        try:
            g = gpd.read_file(gpkg)
        except Exception:
            continue
        if "feature_id" not in g.columns:
            continue
        own = g[pd.to_numeric(g.feature_id, errors="coerce").astype("Int64").isin(feats)]
        if len(own):
            parts.append(own.to_crs(EA))
    if not parts:
        raise SystemExit("no catchment polygon for any treated feature_id in HUC %s: the mask would be "
                         "empty, and an empty mask scores nothing while looking like a valid run" % huc)
    own = gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs="EPSG:%d" % EA)
    geom = own.union_all()
    _CACHE[key] = (geom, float(gpd.GeoSeries([geom], crs=EA).area.iloc[0]) / 1e6)
    return _CACHE[key]


def footprint_mask(root_run, huc, hids, transform, width, height, feats=None):
    """Rasterise the causal footprint onto a grid. True = the slope treatment can act on this pixel."""
    geom, _ = footprint(root_run, huc, hids, feats)
    return ~geometry_mask([geom], out_shape=(height, width), transform=transform, invert=False)


def outside_change(fim_base, fim_treat, root_run, huc, hids, feats=None, grid_m=30.0):
    """THE INVARIANT. Pixels whose wet/dry state differs between baseline and treatment, OUTSIDE the
    catchments the injection touched. Physically this must be zero: the slope was changed nowhere else.

    A non-zero count is a bug, not a result. The cross-branch HydroID collision produced exactly this.
    Returns (n_outside, n_inside, footprint_km2).
    """
    geom, km2 = footprint(root_run, huc, hids, feats)
    with rasterio.open(fim_base) as a, rasterio.open(fim_treat) as b:
        if (a.transform != b.transform) or (a.width, a.height) != (b.width, b.height):
            raise SystemExit("baseline and treatment rasters are not on the same grid; "
                             "a pixel-wise difference would be meaningless")
        wa = a.read(1); wb = b.read(1)
        nda = a.nodata if a.nodata is not None else -9999
        ndb = b.nodata if b.nodata is not None else -9999
        wet_a = np.isfinite(wa) & (wa != nda) & (wa > 0)
        wet_b = np.isfinite(wb) & (wb != ndb) & (wb > 0)
        diff = wet_a ^ wet_b
        inside = ~geometry_mask([geom], out_shape=wa.shape, transform=a.transform, invert=False) \
            if str(a.crs).endswith(str(EA)) else None
        if inside is None:                       # raster is not in EA: reproject the geometry instead
            gser = gpd.GeoSeries([geom], crs=EA).to_crs(a.crs)
            inside = ~geometry_mask([gser.iloc[0]], out_shape=wa.shape, transform=a.transform, invert=False)
    return int((diff & ~inside).sum()), int((diff & inside).sum()), km2
