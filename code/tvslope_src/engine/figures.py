# Map figures: AOI reference maps (SWOT reach, FIMBench flood extent, evaluation domain, gauges).
import numpy as np
import geopandas as gpd, pyogrio, rasterio
from pathlib import Path
from shapely.geometry import Point
from rasterio.warp import transform_bounds, reproject, Resampling
from rasterio.windows import from_bounds as win_from_bounds, Window
from affine import Affine
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from final_config import SWORD
from per_reach3 import P3
from fim_reach import FR
from fim_eval import FE
try:
    import contextily as cx; HAVE_CX = True
except Exception:
    HAVE_CX = False
EA = 5070
GAUGE_NEAR_KM = 0.4

def savefig(fig, path, dpi=300, **kw):
    p = Path(path); kw.setdefault("bbox_inches", "tight")
    fig.savefig(p.with_suffix(".png"), dpi=dpi, **kw)
    fig.savefig(p.with_suffix(".svg"), **kw)
    return p

def reach_geom_ea(reach):
    return pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(reach)}").set_crs(4326, allow_override=True).to_crs(EA).union_all()

def eval_domain(a):
    # evaluation domain = the river mask (union of the reach's NWM catchments), or a 5 km reach buffer if the mask
    # is unavailable; drawn on the AOI maps and scored in Step 11 (rationale in the Step 5 markdown).
    aoi = FR._aoi_dir(str(a.fim_huc8).zfill(8))
    m = FE.river_mask(aoi, a.reach) if aoi else None
    if m is not None: return m, "river_mask"
    return FE.reach_buffer_geom([a.reach], 5.0), "reach_buffer_5km"

def reach_river(a):                                                        # the reach's NWM riverline (for benchmark connectivity)
    aoi = FR._aoi_dir(str(a.fim_huc8).zfill(8))
    return FE.reach_streams(aoi, a.reach) if aoi else None

def flood_overlay(ax, bm_tif, frame3857, target_px=800):
    # overlay the EXACT FIMBench flood extent (benchmark GeoTIFF wet pixels, value>=1) inside the map frame.
    # Windowed + decimated read then warp to 3857, so even a 10^10-pixel benchmark is memory-safe.
    x0, y0, x1, y1 = frame3857
    with rasterio.open(bm_tif) as ds:
        src_crs = ds.crs; tb = transform_bounds("EPSG:3857", src_crs, x0, y0, x1, y1)
        try:                                                       # empty intersection -> benchmark tile does not cover this frame
            win = win_from_bounds(*tb, transform=ds.transform).round_offsets().round_lengths().intersection(Window(0, 0, ds.width, ds.height))
        except Exception:
            return False
        if win.width < 1 or win.height < 1: return False
        ow = int(min(target_px, win.width)); oh = int(min(target_px, win.height))
        arr = ds.read(1, window=win, out_shape=(oh, ow), resampling=Resampling.nearest)
        src_t = ds.window_transform(win) * Affine.scale(win.width/ow, win.height/oh)
    W = target_px; H = max(1, int(round(target_px*(y1-y0)/(x1-x0))))
    dst = np.zeros((H, W), "uint8"); dst_t = rasterio.transform.from_bounds(x0, y0, x1, y1, W, H)
    reproject((arr >= 1).astype("uint8"), dst, src_transform=src_t, src_crs=src_crs, dst_transform=dst_t, dst_crs="EPSG:3857", resampling=Resampling.nearest)
    rgba = np.zeros((H, W, 4)); rgba[dst == 1] = (0.11, 0.42, 0.95, 0.55)
    ax.imshow(rgba, extent=[x0, x1, y0, y1], origin="upper", zorder=3)
    return bool((dst == 1).any())

def latlon_frame(ax, crs=3857, n=3, fs=16):
    import numpy as np
    xt = np.linspace(*ax.get_xlim(), n+2)[1:-1]; yt = np.linspace(*ax.get_ylim(), n+2)[1:-1]
    tx = gpd.GeoSeries([Point(x, y) for x in xt for y in [ax.get_ylim()[0]]], crs=crs).to_crs(4326)
    ty = gpd.GeoSeries([Point(x, y) for y in yt for x in [ax.get_xlim()[0]]], crs=crs).to_crs(4326)
    ax.set_xticks(xt); ax.set_xticklabels([f"{p.x:.2f}°" for p in tx], fontsize=fs)
    ax.set_yticks(yt); ax.set_yticklabels([f"{p.y:.2f}°" for p in ty], fontsize=fs)

if HAVE_CX:                                                # Esri World Hillshade raster (for terrain relief under the Topo basemap)
    import xyzservices
    ESRI_HILLSHADE = xyzservices.TileProvider(name="Esri.WorldHillshade",
        url="https://server.arcgisonline.com/ArcGIS/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}",
        attribution="Esri, USGS, NOAA", max_zoom=19)

def aoi_map(a, eval_geom, out_dir=None, save=True, ax=None, show_legend=True, title_fs=21, title_2line=False, annot_fs=16, tick_fs=16):
    import matplotlib.patheffects as pe
    rl = pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(a.reach)}").set_crs(4326, allow_override=True).to_crs(3857)
    if not len(rl): return None
    own = ax is None                                        # own figure (dossier map) vs. drawn into a shared subplot (2x3 composite)
    if own: fig, ax = plt.subplots(figsize=(8.6, 8.6))
    rl.plot(ax=ax, color="#00e5ff", lw=3.2, zorder=6)
    hnd = [Line2D([], [], color="#00e5ff", lw=3.2, label="SWOT reach"),
           Patch(fc=(0.11, 0.42, 0.95, 0.55), ec="none", label="FIMBench flood extent")]
    # evaluation domain (3857) = the river mask (union of the reach's NWM catchments); drawn as a dashed outline
    ev = gpd.GeoSeries([eval_geom], crs=EA).to_crs(3857).iloc[0]; ex0, ey0, ex1, ey1 = ev.bounds
    cxs, cys = (ex0+ex1)/2, (ey0+ey1)/2; half_sq = max(ex1-ex0, ey1-ey0)/2
    must = [(ex0, ey0), (ex1, ey1), (rl.total_bounds[0], rl.total_bounds[1]), (rl.total_bounds[2], rl.total_bounds[3])]
    for _pp in (ev.geoms if hasattr(ev, "geoms") else [ev]):
        if _pp.geom_type == "Polygon": ax.plot(*_pp.exterior.xy, color="#111111", lw=2.2, ls=(0, (6, 3)), zorder=5)
    hnd.append(Line2D([], [], color="#111111", lw=2.2, ls=(0, (6, 3)), label="evaluation domain (river mask)"))
    # gauges: upstream + downstream (only if genuinely near the reach); id annotated beside the triangle
    rgeo = reach_geom_ea(a.reach)
    for lab, g, col in ([("upstream gauge", a.gup, "#1f77b4"), ("downstream gauge", a.gdn, "#2ca02c")] if a.gauge_paired else []):   # gauges only on the gauge-paired reaches (those with a gauge time-varying S(Q))
        if not (g and str(g) in P3.GC.index): continue
        pea = gpd.GeoSeries([Point(float(P3.GC.loc[g, "gage_longitude"]), float(P3.GC.loc[g, "gage_latitude"]))], crs=4326).to_crs(EA).iloc[0]
        if rgeo.distance(pea) > GAUGE_NEAR_KM*1000: continue      # skip an off-reach gauge (e.g. Neches' 48 km pair)
        p = gpd.GeoSeries([pea], crs=EA).to_crs(3857).iloc[0]
        ax.scatter(p.x, p.y, s=185, marker="^", c=col, ec="k", zorder=7)
        ax.annotate(f"USGS {g}", (p.x, p.y), color="white", fontsize=annot_fs, fontweight="bold",
                    xytext=(9, 6), textcoords="offset points", zorder=8,
                    path_effects=[pe.withStroke(linewidth=3, foreground="black")])
        must.append((p.x, p.y)); hnd.append(Line2D([], [], marker="^", ls="", mfc=col, mec="k", ms=12, label=lab))
    # frame: centre on the evaluation square, include reach + near gauges, with a little context
    need_half = max(max(abs(x-cxs) for x, y in must), max(abs(y-cys) for x, y in must))
    half = max(need_half, half_sq*1.3)*1.12
    ax.set_xlim(cxs-half, cxs+half); ax.set_ylim(cys-half, cys+half)
    if HAVE_CX:
        # Esri "Outdoor" style, rich cartography with an emphasis on the natural world (landcover/biomes, water,
        # parks, roads, railways, cities, admin boundaries) over shaded terrain. The Living-Atlas Outdoor (World
        # Edition) is a vector basemap requiring an ArcGIS token; we reproduce its look with token-free raster tiles:
        # the Esri World Hillshade for terrain relief, overlaid by a semi-transparent Esri World Topographic Map.
        try:
            cx.add_basemap(ax, source=ESRI_HILLSHADE, crs="EPSG:3857", attribution=False, zorder=0)
            cx.add_basemap(ax, source=cx.providers.Esri.WorldTopoMap, crs="EPSG:3857", alpha=0.6, attribution_size=4, zorder=1)
        except Exception: pass
    flood_overlay(ax, a.bm_tif, (cxs-half, cys-half, cxs+half, cys+half))   # exact benchmark flood extent
    latlon_frame(ax, fs=tick_fs)
    _d = str(a.bench_date).replace('-','/')
    ax.set_title((f"{a.river} ({a.reach})\n{_d}" if title_2line else f"{a.river} ({a.reach}), {_d}"), fontsize=title_fs)
    if show_legend:
        ax.legend(handles=hnd, loc="upper center", bbox_to_anchor=(0.5, -0.07), ncol=3, fontsize=15, framealpha=.95)  # below map -> covers no data
    if own and save and out_dir is not None: savefig(fig, out_dir/f"{a.reach}_aoi_map")
    if own: plt.show()
    return hnd
