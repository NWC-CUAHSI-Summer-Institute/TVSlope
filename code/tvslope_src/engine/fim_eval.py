# Categorical FIM-vs-benchmark scoring (FIMeval-style) + River-Mask evaluation domain.
import glob
from pathlib import Path
from types import SimpleNamespace
import numpy as np, pandas as pd
import geopandas as gpd, pyogrio
import rasterio
from rasterio.warp import reproject, Resampling, transform_bounds
from rasterio.windows import from_bounds as _win_from_bounds, Window
from rasterio.features import geometry_mask
from affine import Affine
from scipy import ndimage as _ndi
from final_config import SWORD, EA
from fim_reach import reach_feature_ids
def reach_buffer(reach_ids, buffer_km=5.0):
    if isinstance(reach_ids, (str, int)): reach_ids = [reach_ids]
    geoms = []
    for r in reach_ids:
        try:
            gg = pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(r)}")
            if len(gg): geoms.append(gg.set_crs(4326, allow_override=True).to_crs(EA).geometry.iloc[0])
        except Exception: pass
    if not geoms: return None
    return gpd.GeoSeries(geoms, crs=EA).buffer(buffer_km*1000.0).union_all()
def _grid_for_aoi(aoi_gpkg, grid_m, clip_geom=None):
    if hasattr(aoi_gpkg, "geom_type"):
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
    dst = np.full((height, width), np.nan, dtype="float32")
    with rasterio.open(src_path) as src:
        left, top = transform.c, transform.f
        right, bottom = left + width*transform.a, top + height*transform.e
        try:
            tb = transform_bounds(EA, src.crs, left, bottom, right, top)
            win = _win_from_bounds(*tb, transform=src.transform).round_offsets().round_lengths()
            win = win.intersection(Window(0, 0, src.width, src.height))
        except Exception:
            win = Window(0, 0, src.width, src.height)
        if win.width < 1 or win.height < 1: return dst, src.nodata
        cap = max(int(max(width, height))*4, 2000)                    # source detail cap (~grid/4), memory-safe
        ow = int(min(cap, win.width)); oh = int(min(cap, win.height))
        arr = src.read(band, window=win, out_shape=(oh, ow), resampling=Resampling.nearest).astype("float32")
        src_t = src.window_transform(win) * Affine.scale(win.width/ow, win.height/oh)
        nd = src.nodata
        reproject(arr, dst, src_transform=src_t, src_crs=src.crs, dst_transform=transform, dst_crs=EA,
                  resampling=resampling, src_nodata=nd, dst_nodata=np.nan)
    return dst, nd
def score(fim_tif, bm_tif, aoi_gpkg, grid_m=30.0, min_depth=0.0, clip_geom=None, reach_ids=None, buffer_km=5.0):
    _aoi_ok = (not isinstance(aoi_gpkg, (str, Path))) or Path(aoi_gpkg).exists()
    if not (fim_tif and Path(fim_tif).exists() and Path(bm_tif).exists() and _aoi_ok):
        return dict(error="missing input", CSI=np.nan)
    if clip_geom is None and reach_ids is not None:
        clip_geom = reach_buffer(reach_ids, buffer_km)
    aoi, transform, width, height, _ = _grid_for_aoi(aoi_gpkg, grid_m, clip_geom=clip_geom)
    if width == 0 or height == 0:
        return dict(error="empty domain after clip", CSI=np.nan)
    aoi_mask = ~geometry_mask(aoi.geometry, out_shape=(height, width), transform=transform, invert=False)
    bm, bm_nd = _resample_to_grid(bm_tif, transform, width, height)
    fim, fim_nd = _resample_to_grid(fim_tif, transform, width, height)
    bm_defined = np.isfinite(bm) & (bm != (bm_nd if bm_nd is not None else -9999))
    domain = aoi_mask & bm_defined
    wet_bm = domain & (bm >= 0.5)
    wet_fim = domain & np.isfinite(fim) & (fim != (fim_nd if fim_nd is not None else -9999)) & (fim > min_depth)
    TP = int((wet_fim & wet_bm).sum()); FP = int((wet_fim & ~wet_bm).sum())
    FN = int((~wet_fim & wet_bm).sum()); TN = int((~wet_fim & ~wet_bm & domain).sum())
    csi = TP/(TP+FP+FN) if (TP+FP+FN) else np.nan
    pod = TP/(TP+FN) if (TP+FN) else np.nan
    far = FP/(FP+TP) if (FP+TP) else np.nan
    f1 = 2*TP/(2*TP+FP+FN) if (2*TP+FP+FN) else np.nan
    bias = (TP+FP)/(TP+FN) if (TP+FN) else np.nan
    px_km2 = (grid_m**2)/1e6
    return dict(CSI=round(csi, 4) if csi == csi else np.nan, F1=round(f1, 4) if f1 == f1 else np.nan,
                POD=round(pod, 4) if pod == pod else np.nan,
                FAR=round(far, 4) if far == far else np.nan, bias=round(bias, 4) if bias == bias else np.nan,
                TP=TP, FP=FP, FN=FN, TN=TN, n_domain=int(domain.sum()),
                fim_wet_km2=round(int(wet_fim.sum())*px_km2, 3), bm_wet_km2=round(int(wet_bm.sum())*px_km2, 3),
                grid_m=grid_m)
def score_grids(fim_tif, bm_tif, aoi_gpkg, grid_m=30.0, min_depth=0.0, clip_geom=None, reach_ids=None, buffer_km=5.0):
    if clip_geom is None and reach_ids is not None:
        clip_geom = reach_buffer(reach_ids, buffer_km)
    aoi, transform, width, height, bounds = _grid_for_aoi(aoi_gpkg, grid_m, clip_geom=clip_geom)
    aoi_mask = ~geometry_mask(aoi.geometry, out_shape=(height, width), transform=transform, invert=False)
    bm, bm_nd = _resample_to_grid(bm_tif, transform, width, height)
    fim, fim_nd = _resample_to_grid(fim_tif, transform, width, height)
    bm_defined = np.isfinite(bm) & (bm != (bm_nd if bm_nd is not None else -9999))
    domain = aoi_mask & bm_defined
    wet_bm = domain & (bm >= 0.5)
    wet_fim = domain & np.isfinite(fim) & (fim != (fim_nd if fim_nd is not None else -9999)) & (fim > min_depth)
    cat = np.full((height, width), np.nan, dtype="float32")
    cat[domain & ~wet_fim & ~wet_bm] = 0
    cat[domain & wet_fim & ~wet_bm] = 1
    cat[domain & ~wet_fim & wet_bm] = -1
    cat[domain & wet_fim & wet_bm] = 2
    m = score(fim_tif, bm_tif, aoi_gpkg, grid_m=grid_m, min_depth=min_depth, clip_geom=clip_geom)
    return cat, transform, bounds, m
def _largest_cc(mask):
    if not mask.any(): return mask
    lab, n = _ndi.label(mask)
    if n <= 1: return mask
    sizes = _ndi.sum(mask, lab, range(1, n+1))
    return lab == (int(np.argmax(sizes)) + 1)
def _river_connected(mask, river_px):
    if not mask.any(): return mask
    lab, n = _ndi.label(mask)
    if n < 1: return mask
    touch = np.unique(lab[river_px & (lab > 0)]); touch = touch[touch > 0]
    if len(touch) == 0: return _largest_cc(mask)                 # nothing touches the river -> fall back to largest component
    return np.isin(lab, touch)
def _catchment_file(aoi):
    wd = Path(aoi)/"watershed-data"
    for n in ("nwm_catchments_proj_subset.gpkg", "baseline_catchments_proj_subset.gpkg"):
        if (wd/n).exists(): return wd/n
    c = sorted(wd.glob("*catchments_proj_subset.gpkg")); return c[0] if c else None
def _src_feature_ids(aoi):
    br = Path(aoi)/"watershed-data"/"branches"
    hts = glob.glob(str(br/"*"/"hydroTable_*.csv.orig")) or glob.glob(str(br/"*"/"hydroTable_*.csv"))
    ids = set()
    for h in hts:
        try: ids |= set(int(x) for x in pd.read_csv(h, usecols=["feature_id"])["feature_id"].dropna().astype("int64"))
        except Exception: pass
    return ids
def river_mask(aoi, reach, pad_m=0.0):
    if aoi is None: return None
    fids = set(int(f) for f in reach_feature_ids(aoi, [reach]))
    _src = _src_feature_ids(aoi)
    if _src: fids = fids & _src      # restrict eval domain to catchments HAND modelled (drop no-SRC phantom catchments)
    catf = _catchment_file(aoi)
    if not fids or catf is None: return None
    cat = pyogrio.read_dataframe(catf).to_crs(EA)
    idc = "ID" if "ID" in cat.columns else next((c for c in cat.columns if c.lower() in ("id", "feature_id", "featureid")), None)
    if idc is None: return None
    cat = cat[cat[idc].astype("int64").isin(fids)]
    if not len(cat): return None
    geom = cat.union_all()
    return geom.buffer(pad_m) if pad_m else geom
def reach_streams(aoi, reach):
    if aoi is None: return None
    streams = next((Path(aoi)/"watershed-data").glob("*_subset_streams.gpkg"), None)
    if streams is None: return None
    fids = set(int(f) for f in reach_feature_ids(aoi, [reach]))
    if not fids: return None
    g = pyogrio.read_dataframe(streams).to_crs(EA)
    idc = "ID" if "ID" in g.columns else next((c for c in g.columns if c.lower() in ("id", "feature_id", "featureid")), None)
    if idc is None: return None
    g = g[g[idc].astype("int64").isin(fids)]
    return g.union_all() if len(g) else None
def reach_buffer_geom(reach_ids, km=5.0):
    return reach_buffer(reach_ids, buffer_km=km)
def _resample_win(src_path, transform, width, height, bounds, band=1, resampling=Resampling.nearest):
    with rasterio.open(src_path) as srcd:
        try:
            sb = transform_bounds(EA, srcd.crs, bounds[0], bounds[1], bounds[2], bounds[3])
            win = _win_from_bounds(*sb, transform=srcd.transform).intersection(Window(0, 0, srcd.width, srcd.height))
        except Exception:
            return _resample_to_grid(src_path, transform, width, height, band=band, resampling=resampling)
        if win.width < 1 or win.height < 1: return np.full((height, width), np.nan, "float32"), srcd.nodata
        oh = int(min(win.height, height*4)) or 1; ow = int(min(win.width, width*4)) or 1
        arr = srcd.read(band, window=win, out_shape=(oh, ow), resampling=Resampling.nearest).astype("float32")
        arr_t = srcd.window_transform(win) * Affine.scale(win.width/ow, win.height/oh)
        dst = np.full((height, width), np.nan, "float32")
        reproject(arr, dst, src_transform=arr_t, src_crs=srcd.crs, dst_transform=transform, dst_crs=EA,
                  src_nodata=srcd.nodata, dst_nodata=np.nan, resampling=resampling)
        return dst, srcd.nodata
def score_rm(fim_tif, bm_tif, mask_geom, grid_m=30.0, min_depth=0.0, largest_cc=True, return_grid=False, river_geom=None):
    if not (fim_tif and Path(fim_tif).exists() and bm_tif and Path(bm_tif).exists() and mask_geom is not None):
        return (None, None, None, dict(CSI=np.nan)) if return_grid else dict(CSI=np.nan)
    aoi, transform, width, height, bounds = _grid_for_aoi(mask_geom, grid_m)
    if width == 0 or height == 0:
        return (None, None, None, dict(CSI=np.nan)) if return_grid else dict(CSI=np.nan)
    aoi_mask = ~geometry_mask(aoi.geometry, out_shape=(height, width), transform=transform, invert=False)
    bm, bm_nd = _resample_win(bm_tif, transform, width, height, bounds)
    fim, fim_nd = _resample_to_grid(fim_tif, transform, width, height)
    bm_defined = np.isfinite(bm) & (bm != (bm_nd if bm_nd is not None else -9999))
    domain = aoi_mask & bm_defined
    wet_bm = domain & (bm >= 0.5)
    if river_geom is not None:                                              # keep only benchmark flood connected to the riverline
        try:
            river_px = ~geometry_mask([river_geom], out_shape=(height, width), transform=transform, invert=False)
            wet_conn = _river_connected(wet_bm, river_px)
            dropped  = wet_bm & ~wet_conn                                    # river-disconnected benchmark water (side lakes/ponds)
            domain   = domain & ~dropped                                     # exclude those pixels from the eval entirely (not TP/FP/FN/TN)
            wet_bm   = wet_conn
        except Exception:
            if largest_cc: wet_bm = _largest_cc(wet_bm)
    elif largest_cc:
        wet_bm = _largest_cc(wet_bm)
    wet_fim = domain & np.isfinite(fim) & (fim != (fim_nd if fim_nd is not None else -9999)) & (fim > min_depth)
    TP = int((wet_fim & wet_bm).sum()); FP = int((wet_fim & ~wet_bm & domain).sum())
    FN = int((~wet_fim & wet_bm).sum()); TN = int((~wet_fim & ~wet_bm & domain).sum())
    csi = TP/(TP+FP+FN) if (TP+FP+FN) else np.nan; pod = TP/(TP+FN) if (TP+FN) else np.nan
    far = FP/(FP+TP) if (FP+TP) else np.nan; f1 = 2*TP/(2*TP+FP+FN) if (2*TP+FP+FN) else np.nan
    bias = (TP+FP)/(TP+FN) if (TP+FN) else np.nan; px = (grid_m**2)/1e6
    m = dict(CSI=round(csi, 4) if csi == csi else np.nan, F1=round(f1, 4) if f1 == f1 else np.nan,
             POD=round(pod, 4) if pod == pod else np.nan, FAR=round(far, 4) if far == far else np.nan,
             bias=round(bias, 4) if bias == bias else np.nan, TP=TP, FP=FP, FN=FN, TN=TN,
             n_domain=int(domain.sum()), fim_wet_km2=round(int(wet_fim.sum())*px, 3),
             bm_wet_km2=round(int(wet_bm.sum())*px, 3), grid_m=grid_m)
    if return_grid:
        cat = np.full((height, width), np.nan, dtype="float32")
        cat[domain & ~wet_fim & ~wet_bm] = 0; cat[domain & wet_fim & ~wet_bm] = 1
        cat[domain & ~wet_fim & wet_bm] = -1; cat[domain & wet_fim & wet_bm] = 2
        return cat, transform, bounds, m
    return m
FE  = SimpleNamespace(EA=EA, SWORD=SWORD, score=score, score_grids=score_grids, reach_buffer=reach_buffer,
                      river_mask=river_mask, reach_buffer_geom=reach_buffer_geom, score_rm=score_rm, _largest_cc=_largest_cc, reach_streams=reach_streams)
