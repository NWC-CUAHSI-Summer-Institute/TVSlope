"""The causal footprint of a slope treatment, and the invariant that follows from it.  # sebastian update

WHY THIS EXISTS. The FIMBench benchmark is a multi-source product: it carries lakes, reservoirs,
tributaries and urban flooding that a reach-scale slope change can never move. Scoring the whole scene
therefore SUPPRESSES the slope signal in the ratio. The effect is large: for Neuse reach 73216000121 the
catchments of the injected HydroIDs cover 52.3 km2, while the evaluation box covers about 144 km2.
Roughly two thirds of the scored area is INERT, so every CSI is diluted by a constant and the
differences between treatments are compressed toward zero.

THE DEFENSIBLE MASK is the union of the catchments of the reaches the injector actually modified. That
is the only ground the treatment can act on, it is derivable rather than case-by-case, and it dissolves
the question of what to do about an untouched tributary: an uninjected tributary simply is not in the
mask.

WHAT THE MASK ALSO BUYS: A CORRECTNESS TEST. If the flood map changes OUTSIDE the causal footprint, the
injection touched something it should not have. That is not a metric, it is an invariant, and it is not
hypothetical -- this pipeline shipped a bug where HydroIDs (which HAND numbers PER BRANCH, so the same
integer names a different river in another branch) were used as the injection key, and 52% of the
rescaled rows were the wrong river. `outside_change()` catches exactly that.

WHAT THE MASK COSTS. Masking changes what CSI MEANS. It becomes "skill where the slope can act", not
"flood-map accuracy", so it cannot be compared with published basin-wide HAND-FIM numbers, and a gain on
this domain must never be reported as a basin-scale improvement. Report both.

SELECTION IS BY feature_id, NOT HydroID. The NWM feature_id is globally unique; HAND numbers HydroID per
branch, so HydroIDs collide across branches. And the footprint spans EVERY branch, not just branch 0:
HAND-FIM mosaics the inundation of all branches and each branch carries its own catchment polygons, so a
branch-0-only footprint is incomplete and the invariant then fires false alarms. Measured: a
branch-0-only mask gave the Ouachita a 4.4 km2 footprint and flagged 29,059 "outside" pixels that were
in fact inside the reach's own level-path catchments.

Ported from Sebastian Marshall's `reach_mask.py`, adapted to this repository's fimbox_out layout
(data/fimbox_out/HUC<huc8>/watershed-data/branches/<branch>/) and with SystemExit changed to
RuntimeError so a failure does not kill a Jupyter kernel.

Author of the original analysis: Sebastian R.O. Marshall.
"""

from __future__ import annotations

import glob
import os

import geopandas as gpd
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import geometry_mask

from final_config import EA
from fim_reach import FR

__all__ = ["footprint", "footprint_mask", "outside_change", "reach_footprint"]

_EA_EPSG = int(str(EA).split(":")[-1])          # "EPSG:5070" -> 5070
_CACHE: dict = {}


def _watershed_dir(huc8):
    aoi = FR._aoi_dir(str(huc8).zfill(8))
    if aoi is None:
        raise RuntimeError(f"no staged HAND directory for HUC {huc8}; the footprint cannot be built")
    return os.path.join(str(aoi), "watershed-data")


def footprint(huc8, feats):
    """Union of the catchments of the treated reach, across EVERY branch, in EPSG:5070.

    `feats` are the NWM feature_ids the injector modified -- the crosswalk's own set, the same one
    inject() uses. Deriving them from branch-0 rows instead re-imports the per-branch HydroID collision,
    and then the MASK covers a different set of rivers than the INJECTION does: legitimate changes
    inside the reach land outside the mask and the invariant fires a false alarm.

    Returns (geometry, area_km2).
    """
    feats = set(int(f) for f in feats)
    if not feats:
        raise RuntimeError("footprint() needs at least one feature_id; an empty mask scores nothing "
                           "while looking like a valid run")
    key = (str(huc8), tuple(sorted(feats)))
    if key in _CACHE:
        return _CACHE[key]

    parts = []
    pat = os.path.join(_watershed_dir(huc8), "branches", "*",
                       "gw_catchments_reaches_filtered_addedAttributes_crosswalked_*.gpkg")
    for gpkg in sorted(glob.glob(pat)):
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
        raise RuntimeError(f"no catchment polygon for any treated feature_id in HUC {huc8}: the mask "
                           f"would be empty, and an empty mask scores nothing while looking valid")

    own = gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), crs=EA)
    geom = own.union_all()
    _CACHE[key] = (geom, float(gpd.GeoSeries([geom], crs=EA).area.iloc[0]) / 1e6)
    return _CACHE[key]


def reach_footprint(huc8, reach):
    """The causal footprint of one SWORD reach, resolving its feature_ids through the crosswalk."""
    aoi = FR._aoi_dir(str(huc8).zfill(8))
    feats = FR.reach_feature_ids(aoi, [reach]) if aoi else set()
    return footprint(huc8, feats)


def footprint_mask(huc8, feats, transform, width, height):
    """Rasterise the causal footprint. True = the slope treatment can act on this pixel."""
    geom, _ = footprint(huc8, feats)
    return ~geometry_mask([geom], out_shape=(height, width), transform=transform, invert=False)


def outside_change(fim_base, fim_treat, huc8, feats, verbose=False):
    """THE INVARIANT. Pixels whose wet/dry state differs between baseline and treatment, OUTSIDE the
    catchments the injection touched.

    Physically this must be zero: the slope was changed nowhere else. A non-zero count is a bug, not a
    result -- the cross-branch HydroID collision produced exactly this.

    Returns (n_outside, n_inside, footprint_km2).
    """
    geom, km2 = footprint(huc8, feats)
    with rasterio.open(fim_base) as a, rasterio.open(fim_treat) as b:
        if (a.transform != b.transform) or (a.width, a.height) != (b.width, b.height):
            raise RuntimeError("baseline and treatment rasters are not on the same grid; a pixel-wise "
                               "difference would be meaningless")
        wa, wb = a.read(1), b.read(1)
        nda = a.nodata if a.nodata is not None else -9999
        ndb = b.nodata if b.nodata is not None else -9999
        wet_a = np.isfinite(wa) & (wa != nda) & (wa > 0)
        wet_b = np.isfinite(wb) & (wb != ndb) & (wb > 0)
        diff = wet_a ^ wet_b
        g = geom if str(a.crs).endswith(str(_EA_EPSG)) else gpd.GeoSeries([geom], crs=EA).to_crs(a.crs).iloc[0]
        inside = ~geometry_mask([g], out_shape=wa.shape, transform=a.transform, invert=False)

    n_out, n_in = int((diff & ~inside).sum()), int((diff & inside).sum())
    if verbose:
        print(f"  [invariant] footprint {km2:.1f} km2 | changed inside {n_in} | changed OUTSIDE {n_out}"
              + ("  <-- BUG: the injection touched something it should not have" if n_out else "  OK"))
    return n_out, n_in, km2
