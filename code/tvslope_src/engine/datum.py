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
    "VERTICAL_DATUMS",
    "GEOID_MODELS",
    "USGS_ALT_DATUM",
    "GAUGE_REF_DATUM",
    "convert_vertical",
    "gauge_elevation_to",
    "SWOT_WSE_DATUM",
    "geoid_undulation",
    "ellipsoidal_to_orthometric",
    "orthometric_to_ellipsoidal",
    "convert_geoid",
    "along_channel_slope",
    "geoid_slope_bias",
    "verify_swot_datum",
]

#: Supported vertical datums -> (EPSG code, description, ellipsoid-referenced?).
#:
#: The third field says whether PROJ can relate the datum to the WGS84 ellipsoid. EGM2008,
#: EGM96 and NAVD88 all ship a grid to the ellipsoid, so an undulation is meaningful. NGVD29
#: is a levelling datum with no such grid: PROJ answers such a request with a silent
#: pass-through (h unchanged), which looks plausible and is wrong by ~34 m. So undulations are
#: refused for it, and conversions go through the direct vertical transform instead.
VERTICAL_DATUMS: dict[str, tuple[str, str, bool]] = {
    "egm2008": ("3855", "EGM2008 geoid (SWOT L2_HR_RiverSP reference)",        True),
    "egm96":   ("5773", "EGM96 geoid (MERIT Hydro / SWORD reference)",         True),
    "navd88":  ("5703", "NAVD88 (US national datum; most USGS gauge alt_va)",  True),
    "ngvd29":  ("7968", "NGVD29 (superseded US datum; still on some gauges)",  False),
}

#: Backwards-compatible alias; index 1 is still the description.
GEOID_MODELS = VERTICAL_DATUMS

#: NWIS `alt_datum_cd` -> key in VERTICAL_DATUMS. Anything absent is unusable: "LOCAL" and
#: "ASSUMED" mean the elevation is relative to an arbitrary local mark, so it cannot be
#: differenced against another gauge at all.
USGS_ALT_DATUM: dict[str, str] = {
    "NAVD88": "navd88",
    "NGVD29": "ngvd29",
}

#: The datum gauge water-surface elevations are harmonised onto before differencing.
GAUGE_REF_DATUM = "navd88"

#: The datum SWOT reach/node `wse` is delivered on. Verified empirically --
#: see `verify_swot_datum()`.
SWOT_WSE_DATUM = "egm2008"

_GEOG3D = "EPSG:4979"  # WGS84 lat/lon/ellipsoidal height


def _key(model: str) -> str:
    key = model.lower().replace("-", "").replace("_", "")
    if key not in VERTICAL_DATUMS:
        raise ValueError(
            f"unknown vertical datum {model!r}; choose from {sorted(VERTICAL_DATUMS)}"
        )
    return key


def _code(model: str) -> str:
    return VERTICAL_DATUMS[_key(model)][0]


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
    key = _key(model)
    if not VERTICAL_DATUMS[key][2]:
        raise ValueError(
            f"{model!r} is not ellipsoid-referenced, so it has no undulation. PROJ would answer "
            f"this with a silent pass-through that is wrong by the geoid height (~34 m in CONUS). "
            f"Use convert_vertical() to move heights on or off {model!r}."
        )
    lon, lat = _as_arrays(lon, lat)
    # Transform h = 0: the returned orthometric height is H = 0 - N = -N.
    H = np.asarray(_transformer(key).transform(lon, lat, np.zeros_like(lon))[2], dtype=float)
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
    return convert_vertical(lon, lat, H, src, dst)


def convert_vertical(lon, lat, H, src: str, dst: str) -> np.ndarray:
    """Move a height from one vertical datum to another, at each point.

    Uses PROJ's direct vertical transform between the two compound CRSs, which is the only
    route that works for every datum here: it agrees with going via the ellipsoid to 1e-10 m
    for the geoid models, and it is the *sole* correct route for NGVD29, which has no grid to
    the ellipsoid at all.

    This is the call to reach for before differencing SWOT (EGM2008) against SWORD/MERIT
    (EGM96), or one gauge against another when the two sit on different national datums.
    Points outside the grid come back as NaN.
    """
    lon, lat = _as_arrays(lon, lat)
    H = np.atleast_1d(np.asarray(H, dtype=float))
    if H.size == 1 and lon.size > 1:
        H = np.full(lon.shape, H.item())
    if _key(src) == _key(dst):
        return H.astype(float)
    t = Transformer.from_crs(f"EPSG:4326+{_code(src)}", f"EPSG:4326+{_code(dst)}", always_xy=True)
    out = np.asarray(t.transform(lon, lat, H)[2], dtype=float)
    return np.where(np.isfinite(out), out, np.nan)


def gauge_elevation_to(lon, lat, alt_va_m, alt_datum_cd, target: str = GAUGE_REF_DATUM):
    """Put a USGS gauge datum elevation (`alt_va`) onto `target`.

    NWIS reports `alt_va` against whatever `alt_datum_cd` says -- usually NAVD88, but NGVD29
    is still common, and "LOCAL"/"ASSUMED" mean an arbitrary local mark. Differencing two
    gauges without checking this silently folds the datum offset into the water-surface slope.

    Returns (height_on_target, note). `height` is NaN when the code is missing or unusable,
    and `note` says why, so a caller can drop the pair loudly rather than publish a number.
    """
    code = (str(alt_datum_cd).strip().upper() if alt_datum_cd is not None else "")
    if not code or code in ("NAN", "NONE"):
        return float("nan"), "no alt_datum_cd reported"
    if code not in USGS_ALT_DATUM:
        return float("nan"), f"unusable vertical datum {code!r} (not tied to a national datum)"
    src = USGS_ALT_DATUM[code]
    H = convert_vertical(lon, lat, float(alt_va_m), src, target)[0]
    if not np.isfinite(H):
        return float("nan"), f"{src} -> {target} transform returned no value here"
    return float(H), ("unchanged" if src == _key(target) else f"converted {src} -> {_key(target)}")


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
    print(f"PROJ vertical-datum check at ({lon}, {lat}):")
    for m, (_, _, ellipsoidal) in VERTICAL_DATUMS.items():
        if not ellipsoidal:
            print(f"  N_{m:<8s} = n/a (levelling datum; undulation correctly refused)")
            continue
        n = geoid_undulation(lon, lat, m)[0]
        print(f"  N_{m:<8s} = {n:+9.4f} m" + ("   <-- grid unavailable" if not np.isfinite(n) else ""))

    h = 100.0
    back = orthometric_to_ellipsoidal(lon, lat, ellipsoidal_to_orthometric(lon, lat, h))[0]
    assert abs(back - h) < 1e-6, f"ellipsoid round-trip failed: {back} != {h}"

    H08 = 100.0
    H96 = convert_geoid(lon, lat, H08, "egm2008", "egm96")[0]
    assert abs(convert_geoid(lon, lat, H96, "egm96", "egm2008")[0] - H08) < 1e-6, "geoid round-trip failed"
    print(f"  EGM2008 H={H08:.2f} m  ->  EGM96 H={H96:.4f} m   (diff {H96-H08:+.4f} m)")

    # NGVD29 must go through the direct transform, and must not be a no-op
    shift = convert_vertical(lon, lat, 100.0, "ngvd29", "navd88")[0] - 100.0
    assert np.isfinite(shift) and 0.001 < abs(shift) < 2.0, f"implausible NGVD29->NAVD88 shift {shift}"
    print(f"  NGVD29 -> NAVD88 shift = {shift:+.4f} m")
    try:
        geoid_undulation(lon, lat, "ngvd29"); raise AssertionError("undulation should be refused for ngvd29")
    except ValueError:
        pass

    # a USGS gauge on NGVD29 must be converted; one with a local datum must be refused
    h, note = gauge_elevation_to(lon, lat, 100.0, "NGVD29")
    assert np.isfinite(h) and note.startswith("converted"), note
    _, note_bad = gauge_elevation_to(lon, lat, 100.0, "LOCAL")
    assert not np.isfinite(_), "a LOCAL datum must not produce a height"
    print(f"  gauge NGVD29 100.00 m -> {GAUGE_REF_DATUM} {h:.4f} m ({note}); LOCAL -> refused")

    # a pure offset must not change a slope; a gradient must
    x = np.linspace(0, 10_000, 11)
    assert abs(along_channel_slope(x, 0.001 * x) - 0.001) < 1e-12, "slope fit failed"
    assert abs(along_channel_slope(x, 0.001 * x + 30.0) - 0.001) < 1e-12, "constant offset changed the slope"
    print("  round-trips, slope fit and offset-invariance: OK")
