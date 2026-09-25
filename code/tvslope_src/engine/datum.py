"""Vertical-datum handling for SWOT water-surface elevations and river slope.

Why this module exists
----------------------
A river slope is a *difference* of heights divided by an along-channel distance.
Any constant offset between vertical datums cancels in that difference, so it is
tempting to treat the datum as bookkeeping. It is not. What does **not** cancel is
the along-channel *gradient* of the datum separation, and for the ellipsoid/geoid
separation that gradient is the same order of magnitude as the river slopes this
study is trying to resolve.

Over the 92 SWOT-observed study reaches (median length 10.0 km) the along-channel
EGM2008 geoid gradient has a median magnitude of 4.1 mm/km and reaches 32.9 mm/km.
Measured against the river's own water-surface slope (median 135 mm/km over the 70
reaches whose slope exceeds 10 mm/km), it is worth more than 10 % of the slope on 21
of those 70 reaches and more than half on 3 of them; on 8 of the 92 it exceeds
17 mm/km all by itself -- SWOT's own reach-slope accuracy requirement. Compute a
slope from ellipsoidal heights and that gradient is added to your answer as a
systematic, spatially correlated error: the resulting surface mimics the geoid,
not the river bed.

The practical consequence for this repository
---------------------------------------------
SWOT L2_HR_RiverSP `wse` is **already orthometric on EGM2008** -- it is not an
ellipsoidal height. `verify_swot_datum()` demonstrates this against an independent
orthometric reference rather than asking the reader to take the product
specification on faith. Subtracting a geoid undulation from `wse` "to convert it to
the geoid" is therefore a ~30 m blunder in CONUS, not a refinement.

The datum problem that *is* real here is **mixing models across datasets**: SWOT
reports on EGM2008, SWORD/MERIT Hydro on EGM96, and IRIS on EIGEN-6C4. Differencing
heights that sit on different geoids injects the difference of the two models into
the slope -- a median of 1.2 mm/km and up to 13.0 mm/km between EGM2008 and EGM96
on these reaches. Use `convert_geoid()` to put every source on one model first.

Grids
-----
The transforms use PROJ's vertical-shift grids, downloaded from the PROJ CDN on
first use (`PROJ_NETWORK=ON`, the default in this environment) and cached locally
thereafter. `conda install proj-data` ships them for a fully offline run.
"""

from __future__ import annotations

import numpy as np
from pyproj import Transformer

__all__ = [
    "GEOID_MODELS",
    "SWOT_WSE_DATUM",
    "geoid_undulation",
    "ellipsoidal_to_orthometric",
    "orthometric_to_ellipsoidal",
    "convert_geoid",
    "along_channel_slope",
    "geoid_slope_bias",
    "verify_swot_datum",
]

#: Supported vertical datums -> (compound-CRS EPSG code, human description).
GEOID_MODELS: dict[str, tuple[str, str]] = {
    "egm2008": ("3855", "EGM2008 geoid (SWOT L2_HR_RiverSP reference)"),
    "egm96":   ("5773", "EGM96 geoid (MERIT Hydro / SWORD reference)"),
    "navd88":  ("5703", "NAVD88 (US national datum; USGS gauge alt_va)"),
}

#: The datum SWOT reach/node `wse` is delivered on. Verified empirically --
#: see `verify_swot_datum()`.
SWOT_WSE_DATUM = "egm2008"

_GEOG3D = "EPSG:4979"  # WGS84 lat/lon/ellipsoidal height


def _code(model: str) -> str:
    key = model.lower().replace("-", "").replace("_", "")
    if key not in GEOID_MODELS:
        raise ValueError(
            f"unknown vertical datum {model!r}; choose from {sorted(GEOID_MODELS)}"
        )
    return GEOID_MODELS[key][0]


def _transformer(model: str) -> Transformer:
    return Transformer.from_crs(_GEOG3D, f"EPSG:4326+{_code(model)}", always_xy=True)


def _as_arrays(lon, lat):
    lon = np.atleast_1d(np.asarray(lon, dtype=float))
    lat = np.atleast_1d(np.asarray(lat, dtype=float))
    if lon.shape != lat.shape:
        raise ValueError(f"lon/lat shape mismatch: {lon.shape} vs {lat.shape}")
    return lon, lat


def geoid_undulation(lon, lat, model: str = "egm2008") -> np.ndarray:
    """Geoid undulation N at each point, in metres.

    N is the separation between the WGS84 ellipsoid and the geoid, signed so that

        h_ellipsoidal = H_orthometric + N

    Across CONUS N is about -36 to -8 m, so it is never a negligible term.
    Points outside the grid come back as NaN rather than raising.
    """
    lon, lat = _as_arrays(lon, lat)
    # Transform h = 0: the returned orthometric height is H = 0 - N = -N.
    H = np.asarray(_transformer(model).transform(lon, lat, np.zeros_like(lon))[2], dtype=float)
    N = -H
    return np.where(np.isfinite(N), N, np.nan)


def ellipsoidal_to_orthometric(lon, lat, h_ellipsoidal, model: str = "egm2008") -> np.ndarray:
    """Ellipsoidal (WGS84) height -> orthometric height on `model`: H = h - N."""
    h = np.atleast_1d(np.asarray(h_ellipsoidal, dtype=float))
    return h - geoid_undulation(lon, lat, model)


def orthometric_to_ellipsoidal(lon, lat, H_orthometric, model: str = "egm2008") -> np.ndarray:
    """Orthometric height on `model` -> ellipsoidal (WGS84) height: h = H + N."""
    H = np.atleast_1d(np.asarray(H_orthometric, dtype=float))
    return H + geoid_undulation(lon, lat, model)


def convert_geoid(lon, lat, H, src: str, dst: str) -> np.ndarray:
    """Move an orthometric height from one geoid model to another.

    Goes via the ellipsoid, which is the only datum the two models share:

        H_dst = H_src + N_src - N_dst

    This is the call to reach for before differencing SWOT (EGM2008) against
    SWORD/MERIT (EGM96) or a NAVD88 gauge elevation.
    """
    H = np.atleast_1d(np.asarray(H, dtype=float))
    return H + geoid_undulation(lon, lat, src) - geoid_undulation(lon, lat, dst)


def along_channel_slope(dist_m, height_m) -> float:
    """Least-squares along-channel slope dH/dx in m/m (NaN if under-determined).

    `dist_m` is an along-channel coordinate that increases upstream (SWORD's
    `dist_out` does), so a normal river returns a positive slope.
    """
    x = np.asarray(dist_m, dtype=float)
    y = np.asarray(height_m, dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 2 or np.ptp(x[ok]) == 0:
        return float("nan")
    return float(np.polyfit(x[ok], y[ok], 1)[0])


def geoid_slope_bias(lon, lat, dist_m, model: str = "egm2008") -> float:
    """Along-channel geoid gradient dN/dx in m/m.

    This is exactly the spurious slope you inherit by computing a water-surface
    slope from ellipsoidal heights instead of orthometric ones. Multiply by 1e6
    to read it in mm/km and compare against the river slope.
    """
    return along_channel_slope(dist_m, geoid_undulation(lon, lat, model))


def verify_swot_datum(swot_wse, reference_H, lon, lat, reference_model: str = "egm96") -> dict:
    """Decide empirically whether SWOT `wse` is orthometric or ellipsoidal.

    Scores two competing hypotheses against an independent orthometric reference
    (SWORD/MERIT `wse`, EGM96, works well) and returns the median residual of each:

    * ``orthometric``  -- `wse` is already on the geoid; compare it directly.
    * ``ellipsoidal``  -- `wse` is an ellipsoidal height; subtract N first.

    The verdict is whichever hypothesis leaves the smaller absolute median
    residual. On the study reaches the margin is decisive: 0.41 m against 29.23 m.
    """
    wse = np.atleast_1d(np.asarray(swot_wse, dtype=float))
    ref = np.atleast_1d(np.asarray(reference_H, dtype=float))
    ref_on_swot_model = convert_geoid(lon, lat, ref, reference_model, SWOT_WSE_DATUM)
    N = geoid_undulation(lon, lat, SWOT_WSE_DATUM)

    resid_ortho = wse - ref_on_swot_model
    resid_ellip = (wse - N) - ref_on_swot_model
    ok = np.isfinite(resid_ortho) & np.isfinite(resid_ellip)
    m_ortho = float(np.median(resid_ortho[ok]))
    m_ellip = float(np.median(resid_ellip[ok]))

    return {
        "n": int(ok.sum()),
        "median_residual_if_orthometric_m": m_ortho,
        "median_residual_if_ellipsoidal_m": m_ellip,
        "verdict": "orthometric" if abs(m_ortho) < abs(m_ellip) else "ellipsoidal",
        "margin_m": abs(abs(m_ellip) - abs(m_ortho)),
    }


if __name__ == "__main__":
    # Self-check: confirms PROJ can reach the geoid grids and that the transforms are
    # self-consistent. Run with:  python code/tvslope_src/engine/datum.py
    lon, lat = -88.0, 37.0
    print(f"PROJ geoid check at ({lon}, {lat}):")
    for m in GEOID_MODELS:
        n = geoid_undulation(lon, lat, m)[0]
        print(f"  N_{m:<8s} = {n:+9.4f} m" + ("   <-- grid unavailable" if not np.isfinite(n) else ""))

    h = 100.0
    back = orthometric_to_ellipsoidal(lon, lat, ellipsoidal_to_orthometric(lon, lat, h))[0]
    assert abs(back - h) < 1e-6, f"ellipsoid round-trip failed: {back} != {h}"

    H08 = 100.0
    H96 = convert_geoid(lon, lat, H08, "egm2008", "egm96")[0]
    assert abs(convert_geoid(lon, lat, H96, "egm96", "egm2008")[0] - H08) < 1e-6, "geoid round-trip failed"
    print(f"  EGM2008 H={H08:.2f} m  ->  EGM96 H={H96:.4f} m   (diff {H96-H08:+.4f} m)")

    # a pure offset must not change a slope; a gradient must
    x = np.linspace(0, 10_000, 11)
    assert abs(along_channel_slope(x, 0.001 * x) - 0.001) < 1e-12, "slope fit failed"
    assert abs(along_channel_slope(x, 0.001 * x + 30.0) - 0.001) < 1e-12, "constant offset changed the slope"
    print("  round-trips, slope fit and offset-invariance: OK")
