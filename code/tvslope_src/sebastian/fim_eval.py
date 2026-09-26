"""FIMeval-lite: score a FIMbox inundation extent against a FIMBench benchmark map on a common grid,
restricted to the benchmark event's AOI polygon. Standard categorical flood-map metrics.

Benchmark encoding (FIMBench *_BM.tif): 1 = wet, 0 = dry, -9999 = nodata/outside. EPSG:4326.
FIM extent: the OWP SIGNED HydroID raster (positive HydroID = wet, negative = dry), NOT a depth raster. Wet is a sign test. This sentence was previously wrong and is what made min_depth look like a safe metres-valued knob.

Metrics over the domain = (inside AOI polygon) AND (benchmark defined, BM != nodata):
    CSI = TP/(TP+FP+FN)   POD = TP/(TP+FN)   FAR = FP/(FP+TP)   bias = (TP+FP)/(TP+FN)
where wet is the positive class. We resample onto an equal-area (EPSG:5070) grid at `grid_m` so pixel
counts are areally fair and the two very different native resolutions are comparable.
"""
import warnings; warnings.filterwarnings("ignore")
import os; os.environ.pop("PROJ_DATA", None); os.environ.pop("PROJ_LIB", None)
from pathlib import Path
import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling, transform_bounds
from rasterio.features import geometry_mask
import geopandas as gpd, pyogrio
from pathlib import Path as _Path

EA = "EPSG:5070"   # CONUS Albers equal-area (metres)


def permanent_water(aoi_gpkg, transform, width, height, cache_dir=None, streams_gpkg=None):
    """Boolean permanent-water mask on the target grid, from fimeval's own extractor.

    THE BUG THIS FIXES. The FIMBench benchmarks are OBSERVED-WATER maps, so they contain the river sitting
    in its own channel. Those pixels are not a flood. Inside cell 44's own 12 km box on the Ohio they are
    12,774 of 25,906 benchmark-wet pixels, i.e. 49.3% of everything the benchmark calls wet. A HAND-FIM that
    leaves the channel dry therefore puts every one of them in FN, and the map paints the whole river blue as
    a missed flood. Cell 44 printed POD 0.519 for the Ohio baseline, which implies an FN share of 48.1%. That
    matches the measured permanent-water share to 1.2%. Its entire "miss" class was the river.

    The operational scorer does not do this. fimeval gives permanent water its own class (5) and excludes it:
    fimeval/ContingencyMap/metrics.py:12-15 reads only classes 1 to 4. This reuses fimeval's own extractor so
    the definition matches the operational product exactly.

    The mask is CACHED because ExtractPWB queries a live ArcGIS endpoint. An empty response would silently
    reintroduce the defect, so an empty result raises rather than returning a blank mask."""
    import hashlib as _hl
    import os as _os
    import geopandas as _gpd
    from rasterio.features import rasterize as _rasterize
    import fimeval as _fe

    # `aoi_gpkg` is whatever _grid_for_aoi accepts: a gpkg path, a GeoDataFrame, or a bare shapely geometry
    # already in EPSG:5070 (cell 44 passes EVAL_GEOM[reach], which is the last of those). ExtractPWB takes a
    # path or a GeoDataFrame, so a geometry is wrapped before it is handed over.
    if hasattr(aoi_gpkg, "geom_type"):                      # shapely geometry in EA
        boundary = _gpd.GeoDataFrame(geometry=[aoi_gpkg], crs=EA)
        key = _hl.md5(aoi_gpkg.wkb).hexdigest()[:16]
    elif isinstance(aoi_gpkg, _gpd.GeoDataFrame):
        boundary = aoi_gpkg.to_crs(EA)
        # Key on the GEOMETRY, not the bounding box: two differently shaped AOIs sharing a bbox used to
        # collide and reuse each other's permanent water. sorted() also mixed x and y ordinates.
        key = _hl.md5(boundary.geometry.union_all().wkb).hexdigest()[:16]
    else:
        boundary = str(aoi_gpkg)
        key = _os.path.basename(boundary).replace(".gpkg", "")

    cache_dir = cache_dir or str(_resolve_root() / "data" / "pwb_cache")
    _os.makedirs(cache_dir, exist_ok=True)
    cache = _os.path.join(cache_dir, f"{key}_pwb.gpkg")
    if not _os.path.exists(cache):
        _fe.ExtractPWB(boundary=boundary, output_dir=cache_dir, save=True,
                       output_filename=_os.path.basename(cache))
    if not _os.path.exists(cache):
        raise RuntimeError(f"ExtractPWB wrote no permanent-water file for {key}. Refusing to score.")
    g = _gpd.read_file(cache) if _os.path.exists(cache) else _gpd.GeoDataFrame(geometry=[])
    if not len(g):
        # LOCAL FALLBACK: the live ArcGIS ExtractPWB returns nothing for some small Midwest AOIs that carry
        # no mapped lakes. That is not necessarily a service failure: for a small perennial creek the
        # permanent water IS the river channel itself. So fall back to the NWM stream network (the operational
        # river lines), buffered to a nominal channel half-width, clipped to the AOI. This directly encodes
        # the original "the river should be permanent water, not a missed flood" insight, from a local source.
        if streams_gpkg and _os.path.exists(streams_gpkg):
            _bnd = boundary if hasattr(boundary, "geometry") else _gpd.read_file(boundary)
            _aoi = _bnd.to_crs(EA).union_all()
            _st = _gpd.read_file(streams_gpkg).to_crs(EA)
            _st = _st[_st.geometry.intersects(_aoi)]
            if len(_st):
                g = _gpd.GeoDataFrame(geometry=[_st.buffer(20.0).union_all().intersection(_aoi)], crs=EA)
                print("  [PWB] ExtractPWB empty; using local NWM-stream channel (%d reaches, 20 m buffer)"
                      % len(_st), flush=True)
        if not len(g):
            raise RuntimeError(
                "ExtractPWB returned no permanent water and no local NWM stream fallback was available. "
                "Refusing to score: an empty mask makes the river count as a missed flood, the exact defect "
                "this guards against.")
    g = g.to_crs(EA)
    geoms = [x for x in g.geometry if x is not None and not x.is_empty]
    if not geoms:
        # RAISE, do not hand back a blank mask. A PWB cache with rows but no valid geometry (a truncated or
        # partial write) passes the row-count guard above, and a blank PERM makes `domain & ~perm` a no-op:
        # the river channel goes straight back to being scored as a "missed flood". That is the 49.3%-of-
        # benchmark-wet bug this module exists to prevent, and it would return a plausible CSI with no error.
        raise SystemExit("permanent-water layer has rows but no valid geometry: refusing to score with an "
                         "empty PERM mask, which would score the river channel as missed flood")
    return _rasterize(((x, 1) for x in geoms), out_shape=(height, width), transform=transform,
                      fill=0, dtype="uint8").astype(bool)


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


SWORD = _resolve_root() / "data" / "SWORD_v17b_gpkg" / "na_sword_reaches_v17b.gpkg"


def reach_buffer(reach_ids, buffer_km=5.0):
    """Union of `buffer_km` buffers around the SWORD centerline(s) of `reach_ids`, returned in EPSG:5070.
    This is the riverine evaluation domain: FIM benchmarks (esp. coastal HWM) cover huge basins that include
    storm-surge/pluvial water HAND-FIM cannot represent, so slope-sensitivity CSI must be scored near the
    modeled channel, not over the whole AOI."""
    if isinstance(reach_ids, (str, int)): reach_ids = [reach_ids]
    geoms = []
    for r in reach_ids:
        try:
            gg = pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(r)}")
            if len(gg): geoms.append(gg.set_crs(4326, allow_override=True).to_crs(EA).geometry.iloc[0])
        except Exception as _e:
            # Do NOT swallow this. Returning None makes score() fall back to clip_geom=None and score the WHOLE
            # AOI instead of the river corridor, so one site gets a corridor domain and another a basin domain
            # and their CSI values are not comparable. Fail loudly instead of silently changing the denominator.
            raise SystemExit("reach_buffer failed for reach %s: %s. Refusing to silently fall back to the "
                             "full-AOI domain, which is not comparable across sites." % (rid, _e))
    if not geoms: return None
    gs = gpd.GeoSeries(geoms, crs=EA).buffer(buffer_km*1000.0)
    return gs.union_all()


def _grid_for_aoi(aoi_gpkg, grid_m, clip_geom=None):
    """Target grid (transform, width, height, bounds) in EPSG:5070 covering the AOI, optionally intersected with
    clip_geom. `aoi_gpkg` may be a gpkg path, a GeoDataFrame, or a shapely geometry already in EPSG:5070."""
    if hasattr(aoi_gpkg, "geom_type"):                       # a shapely geometry in EPSG:5070 (e.g. the eval box)
        aoi = gpd.GeoDataFrame(geometry=[aoi_gpkg], crs=EA)
    elif isinstance(aoi_gpkg, gpd.GeoDataFrame):
        aoi = aoi_gpkg.to_crs(EA)
    else:
        aoi = pyogrio.read_dataframe(aoi_gpkg).to_crs(EA)
    if clip_geom is not None:
        aoi = gpd.GeoDataFrame(geometry=[aoi.union_all().intersection(clip_geom)], crs=EA)
        aoi = aoi[~aoi.geometry.is_empty]
    minx, miny, maxx, maxy = aoi.total_bounds
    minx = np.floor(minx/grid_m)*grid_m; miny = np.floor(miny/grid_m)*grid_m
    maxx = np.ceil(maxx/grid_m)*grid_m;  maxy = np.ceil(maxy/grid_m)*grid_m
    width = int(round((maxx-minx)/grid_m)); height = int(round((maxy-miny)/grid_m))
    transform = rasterio.transform.from_origin(minx, maxy, grid_m, grid_m)
    return aoi, transform, width, height, (minx, miny, maxx, maxy)


def _resample_to_grid(src_path, transform, width, height, band=1, resampling=Resampling.nearest):
    """Read `src_path`, reproject its band onto the target 5070 grid. Returns (data, src_nodata)."""
    with rasterio.open(src_path) as src:
        dst = np.full((height, width), np.nan, dtype="float32")
        reproject(source=rasterio.band(src, band), destination=dst,
                  src_transform=src.transform, src_crs=src.crs,
                  dst_transform=transform, dst_crs=EA, resampling=resampling,
                  src_nodata=src.nodata, dst_nodata=np.nan)
        return dst, src.nodata


def score(fim_tif, bm_tif, aoi_gpkg, grid_m=30.0, min_depth=0.0, clip_geom=None, reach_ids=None, buffer_km=5.0, streams_gpkg=None):
    """Categorical scores of a FIM extent vs a FIMBench benchmark within the AOI (optionally restricted to a
    reach buffer). Pass reach_ids to auto-build the buffer, or clip_geom (5070) directly. Returns a dict with
    CSI/POD/FAR/bias, the contingency counts, and wet-area (km^2) for FIM and benchmark."""
    _aoi_ok = (not isinstance(aoi_gpkg, (str, Path))) or Path(aoi_gpkg).exists()   # geometry/GDF, or an existing gpkg
    if not (fim_tif and Path(fim_tif).exists() and Path(bm_tif).exists() and _aoi_ok):
        return dict(error="missing input", CSI=np.nan)
    if clip_geom is None and reach_ids is not None:
        clip_geom = reach_buffer(reach_ids, buffer_km)
    aoi, transform, width, height, _ = _grid_for_aoi(aoi_gpkg, grid_m, clip_geom=clip_geom)
    if width == 0 or height == 0:
        return dict(error="empty domain after clip", CSI=np.nan)
    aoi_mask = ~geometry_mask(aoi.geometry, out_shape=(height, width), transform=transform, invert=False)
    bm, bm_nd = _resample_to_grid(bm_tif, transform, width, height)         # 1 wet / 0 dry / nan outside
    fim, fim_nd = _resample_to_grid(fim_tif, transform, width, height)      # depth/extent
    bm_defined = np.isfinite(bm) & (bm != (bm_nd if bm_nd is not None else -9999))
    perm = permanent_water(aoi_gpkg, transform, width, height, streams_gpkg=streams_gpkg) & aoi_mask & bm_defined
    domain = aoi_mask & bm_defined & ~perm          # permanent water is mapped, never scored
    wet_bm = domain & (bm >= 0.5)
    # The FIM is NOT a depth raster: it is the OWP SIGNED HydroID raster (inundation.py:366 flips dry
    # pixels negative), so positive HydroID = wet and negative = dry. `fim > min_depth` therefore compares
    # a CATCHMENT ID against a depth in metres. Applying a routine 0.3 m depth filter changes NOTHING
    # (measured: identical wet-pixel count at 0.0, 0.1, 0.3 and 0.99 m), while 2.0 m silently deletes
    # HydroID 1, filtering by ID number. Wet is a SIGN test, and the knob is refused rather than lying.
    if min_depth:
        raise SystemExit("min_depth is meaningless here: the FIM is a signed-HydroID raster, not depth. "
                         "Wet is fim > 0. Filter depth upstream if you need it.")
    wet_fim = domain & np.isfinite(fim) & (fim != (fim_nd if fim_nd is not None else -9999)) & (fim > 0)
    TP = int((wet_fim & wet_bm).sum()); FP = int((wet_fim & ~wet_bm).sum())
    FN = int((~wet_fim & wet_bm).sum()); TN = int((~wet_fim & ~wet_bm & domain).sum())
    PERM = int(perm.sum())
    csi = TP/(TP+FP+FN) if (TP+FP+FN) else np.nan
    pod = TP/(TP+FN) if (TP+FN) else np.nan
    far = FP/(FP+TP) if (FP+TP) else np.nan
    f1 = 2*TP/(2*TP+FP+FN) if (2*TP+FP+FN) else np.nan     # F1 = 2*CSI/(1+CSI) (Dice); precision=1-FAR, recall=POD
    bias = (TP+FP)/(TP+FN) if (TP+FN) else np.nan
    px_km2 = (grid_m**2)/1e6
    return dict(CSI=round(csi, 4) if csi == csi else np.nan, F1=round(f1, 4) if f1 == f1 else np.nan,
                POD=round(pod, 4) if pod == pod else np.nan,
                FAR=round(far, 4) if far == far else np.nan, bias=round(bias, 4) if bias == bias else np.nan,
                TP=TP, FP=FP, FN=FN, TN=TN, PERM=PERM, n_domain=int(domain.sum()),
                fim_wet_km2=round(int(wet_fim.sum())*px_km2, 3), bm_wet_km2=round(int(wet_bm.sum())*px_km2, 3),
                perm_km2=round(PERM*px_km2, 3), grid_m=grid_m)


def score_grids(fim_tif, bm_tif, aoi_gpkg, grid_m=30.0, min_depth=0.0, clip_geom=None, reach_ids=None, buffer_km=5.0, streams_gpkg=None):
    """Like score() but also returns the categorical map plus the 5070 transform, for plotting.

    Class codes now match fimeval's own (ContingencyMap/printcontingency.py:47), so these rasters and their
    legend line up with any FIMBench output instead of needing a private key:

        0 outside | 1 TN | 2 FP | 3 FN | 4 TP | 5 permanent water (drawn, excluded from every metric)

    The old codes were 0=TN, 1=FP, -1=FN, 2=TP, with no class for permanent water at all."""
    if clip_geom is None and reach_ids is not None:
        clip_geom = reach_buffer(reach_ids, buffer_km)
    aoi, transform, width, height, bounds = _grid_for_aoi(aoi_gpkg, grid_m, clip_geom=clip_geom)
    aoi_mask = ~geometry_mask(aoi.geometry, out_shape=(height, width), transform=transform, invert=False)
    bm, bm_nd = _resample_to_grid(bm_tif, transform, width, height)
    fim, fim_nd = _resample_to_grid(fim_tif, transform, width, height)
    bm_defined = np.isfinite(bm) & (bm != (bm_nd if bm_nd is not None else -9999))
    perm = permanent_water(aoi_gpkg, transform, width, height, streams_gpkg=streams_gpkg) & aoi_mask & bm_defined
    domain = aoi_mask & bm_defined & ~perm
    wet_bm = domain & (bm >= 0.5)
    # The FIM is NOT a depth raster: it is the OWP SIGNED HydroID raster (inundation.py:366 flips dry
    # pixels negative), so positive HydroID = wet and negative = dry. `fim > min_depth` therefore compares
    # a CATCHMENT ID against a depth in metres. Applying a routine 0.3 m depth filter changes NOTHING
    # (measured: identical wet-pixel count at 0.0, 0.1, 0.3 and 0.99 m), while 2.0 m silently deletes
    # HydroID 1, filtering by ID number. Wet is a SIGN test, and the knob is refused rather than lying.
    if min_depth:
        raise SystemExit("min_depth is meaningless here: the FIM is a signed-HydroID raster, not depth. "
                         "Wet is fim > 0. Filter depth upstream if you need it.")
    wet_fim = domain & np.isfinite(fim) & (fim != (fim_nd if fim_nd is not None else -9999)) & (fim > 0)
    cat = np.zeros((height, width), dtype="uint8")
    cat[domain & ~wet_fim & ~wet_bm] = 1     # TN
    cat[domain & wet_fim & ~wet_bm] = 2      # FP false alarm
    cat[domain & ~wet_fim & wet_bm] = 3      # FN miss
    cat[domain & wet_fim & wet_bm] = 4       # TP hit
    cat[perm] = 5                            # permanent water: drawn, never scored
    m = score(fim_tif, bm_tif, aoi_gpkg, grid_m=grid_m, min_depth=min_depth, clip_geom=clip_geom)
    return cat, transform, bounds, m
