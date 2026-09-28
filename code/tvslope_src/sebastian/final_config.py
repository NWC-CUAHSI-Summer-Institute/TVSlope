"""work6_final · the focused 6-area study configuration (drives the 13-step work6_3DHRS notebook).

Six study areas (the old 15+5 selection is retained in study_areas_final.csv but superseded here):
  · 2 GAUGE-PAIRED  -> build the time-varying gauge-slope SRC (paired-station S(Q) -> Manning): Illinois
                       74282100101 (kinematic, R2=0.89) + Ohio 74267300251 (backwater, R2=0.99)
  · 2 BACKWATER     -> slope FLATTENS as flow rises (rho(slope,stage) < 0): Mississippi + Ohio
  · KINEMATIC       -> slope STEEPENS as flow rises (rho > 0): Illinois x2 + Neches x2

Gauge notes: Neches 75120400053's working pair (08040600 Rockland / 08041000 Evadale) is 48.7 km apart -> NOT
gauge-paired (reach is a sliver on the map). Mississippi 74270100061's twin-gauge slope is flat and datum-
dominated (R2=0.08) even after IV->daily aggregation -> NOT gauge-paired. Both are scored with static/SWOT slopes.
Big rivers publish stage as instantaneous only; per_reach3.stage_series/discharge now fall back to IV daily-mean.
"""
import os
from pathlib import Path
import pandas as pd

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


ROOT = _resolve_root()
OUT  = ROOT/"output_final"                      # all new outputs live here; output_exp6 is left untouched
TAB, FIG, DOSS, PAP = OUT/"tables", OUT/"figures", OUT/"dossier", OUT/"paper"
for d in (TAB, FIG, DOSS, PAP): d.mkdir(parents=True, exist_ok=True)

# reach, fim_huc8, river, bench_date, dyn_class, role, gauge_paired, gup, gdn(on-reach Q), gq(discharge gauge), csi_ok, fim_driver
# fim_driver: "nwm" = FIM driven by NWM-retrospective discharge at the bench_date (in-retrospective events);
#             "gauge" = FIM driven by the on-reach USGS gauge discharge at the bench_date (for events past the
#             NWM retrospective, e.g. Ohio 2025) — consistent with the gauge-slope method, so it is still scored.
# gq = the on-reach gauge nearest the observed flood; its discharge at bench_date drives the gauge time-varying
#      S(Q) FIM on gauge-paired reaches (Illinois 2016 flood is at the UPSTREAM end -> gq = upstream gauge 05586100).
AREAS = [
    # Neches 053: working twin gauges (08040600/08041000) are 48.7 km apart -> the SWOT reach is a tiny sliver on
    # the map and the "slope" spans far more than the reach. Dropped from gauge-paired; kept as a kinematic reach.
    dict(reach="75120400053", huc="12020003", river="Neches River",      bench_date="2017-09-01",
         dyn="kinematic", role="kinematic",   gauge_paired=False, gup="08040600", gdn="08041000", gq="08041000", csi_ok=True,  fim_driver="nwm"),
    # Illinois 101: the 2016 flood sits at the UPSTREAM end of the reach, so the gauge time-varying S(Q) FIM is
    # driven by the nearest on-reach gauge — the upstream 05586100 (3200 m3/s on 2016-01-04). Constant treatments
    # (IRIS-SWORD, SWOT-*) remain NWM-driven (in-retrospective), so fim_driver stays "nwm".
    dict(reach="74282100101", huc="07130011", river="Illinois River",    bench_date="2016-01-04",
         dyn="kinematic", role="gauge-paired", gauge_paired=True,  gup="05586100", gdn="05586300", gq="05586100", csi_ok=True,  fim_driver="nwm"),
    dict(reach="74270100061", huc="07140105", river="Mississippi River", bench_date="2017-05-04", bench_huc="08010300",
         dyn="backwater",  role="backwater",    gauge_paired=False, gup="07020850", gdn="07022000", gq="07022000", csi_ok=True,  fim_driver="nwm"),
    # Ohio below McAlpine Dam = a textbook BACKWATER (slope falls as flow rises, rho(Q,S)=-1.00, S(Q) R2=0.99),
    # gauge-paired, so it exercises the time-varying method on a backwater regime. Its 2025 benchmark is past the
    # NWM retrospective, so its FIM is driven by the on-reach gauge discharge (15631 m3/s on 2025-04-12) and IS
    # scored vs the 2025 benchmark. Only in-retrospective backwater otherwise is Mississippi 2017.
    dict(reach="74267300251", huc="05140101", river="Ohio River",        bench_date="2025-04-12",
         dyn="backwater",  role="backwater",    gauge_paired=True,  gup="03293551", gdn="03294500", gq="03294500", csi_ok=True,  fim_driver="gauge"),
    dict(reach="74282100111", huc="07130011", river="Illinois River",    bench_date="2016-01-04",
         dyn="kinematic", role="kinematic",    gauge_paired=False, gup=None,        gdn="05585500", gq="05585500", csi_ok=True,  fim_driver="nwm"),
    dict(reach="75120400151", huc="12020003", river="Neches River",      bench_date="2017-09-01",
         dyn="kinematic", role="kinematic",    gauge_paired=False, gup=None,        gdn="08040600", gq="08040600", csi_ok=True,  fim_driver="nwm"),
    # ---- NEW AREAS (Neuse / Louisiana / Caloosahatchee), added 2026-07-14 ----
    # Three well-defined riverine floods with a DYNAMIC SWOT slope (p95/p05 = 2.5x to 264x).
    # The Mississippi above has p95/p05 = 1.3: its five treatments differ by 0.016 CSI, so it
    # cannot test a time-varying slope at all. These can.
    dict(reach="73216000121", huc="03020201", river="Neuse River", bench_date="2016-10-09",
         dyn="dynamic", role="neuse", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="73216000141", huc="03020201", river="Neuse River", bench_date="2016-10-09",
         dyn="dynamic", role="neuse", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="73216000161", huc="03020201", river="Neuse River", bench_date="2016-10-09",
         dyn="dynamic", role="neuse", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    # Reaches 73216000171 and 73216000181 are DROPPED from the Matthew set. The Neuse folder holds three
    # HWM scenes, and those two reaches fall inside only the Hurricane FLORENCE footprint
    # (HWM_20180831_20180918_782136W352113N). No Matthew benchmark covers them, so for bench_date
    # 2016-10-09 they cannot be scored against an observation of that flood. They are candidates for a
    # separate Florence-2018 event, not for this one.
    dict(reach="73216000191", huc="03020201", river="Neuse River", bench_date="2016-10-09",
         dyn="dynamic", role="neuse", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="73216000201", huc="03020201", river="Neuse River", bench_date="2016-10-09",
         dyn="dynamic", role="neuse", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="73216000211", huc="03020201", river="Neuse River", bench_date="2016-10-09",
         dyn="dynamic", role="neuse", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="73257400023", huc="03090205", river="Caloosahatchee River", bench_date="2022-09-30",
         dyn="dynamic", role="caloosahatchee", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="73257400031", huc="03090205", river="Caloosahatchee River", bench_date="2022-09-30",
         dyn="dynamic", role="caloosahatchee", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="74222700141", huc="08040202", river="Ouachita River", bench_date="2016-03-13",
         dyn="dynamic", role="louisiana", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="74222700151", huc="08040202", river="Ouachita River", bench_date="2016-03-13",
         dyn="dynamic", role="louisiana", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
    dict(reach="74222700231", huc="08040202", river="Bayou D'Arbonne", bench_date="2016-03-13",
         dyn="dynamic", role="louisiana", gauge_paired=False, gup=None, gdn=None, gq=None,
         csi_ok=True, fim_driver="nwm"),
]

# slope TREATMENTS scored on each area (baseline first). gauge time-varying only where gauge_paired.
TREATMENTS = ["baseline", "hfirissword_new", "swot_median", "swot_floodstage", "swot_maxwse", "gauge_timevarying"]
BASELINE   = "hfirissword_new"                  # operational static-satellite baseline (Chen 2025)

TREAT_LABEL = {"baseline": "hydrofabric", "hfirissword_new": "IRIS-SWORD", "swot_median": "SWOT-median",
               "swot_floodstage": "SWOT-floodstage", "swot_maxwse": "SWOT-maxWSE",
               "gauge_timevarying": "gauge time-varying S(Q)"}
TREAT_COLOR = {"baseline": "#777777", "hfirissword_new": "#33bbee", "swot_median": "#0077bb",
               "swot_floodstage": "#ee3377", "swot_maxwse": "#ee7733", "gauge_timevarying": "#009988"}
DYN_COLOR   = {"kinematic": "#0077bb", "backwater": "#ee7733", "stable": "#999999"}


def _gauge_span_km(gup, gdn):
    """Great-circle distance (km) between two USGS gauges, from per_reach3.GC coords. 0 if unavailable."""
    try:
        import per_reach3 as P3, numpy as np
        if not gup or not gdn or gup not in P3.GC.index or gdn not in P3.GC.index: return 0.0
        la1, lo1 = float(P3.GC.loc[gup, "gage_latitude"]), float(P3.GC.loc[gup, "gage_longitude"])
        la2, lo2 = float(P3.GC.loc[gdn, "gage_latitude"]), float(P3.GC.loc[gdn, "gage_longitude"])
        r = 6371.0; p1, p2 = np.radians(la1), np.radians(la2); dphi = np.radians(la2-la1); dlmb = np.radians(lo2-lo1)
        h = np.sin(dphi/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dlmb/2)**2
        return float(2*r*np.arcsin(np.sqrt(h)))
    except Exception:
        return 0.0


_BM_CACHE = {}
_REACH_CACHE = {}


def _reach_ll(reach):
    """The reach centerline in EPSG:4326, cached. Used to test which benchmark scene actually covers it."""
    if reach not in _REACH_CACHE:
        import pyogrio
        sw = ROOT/"data"/"SWORD_v17b_gpkg"/"na_sword_reaches_v17b.gpkg"
        g = pyogrio.read_dataframe(sw, where="reach_id = %d" % int(reach)).set_crs(4326, allow_override=True)
        _REACH_CACHE[reach] = g.union_all()
    return _REACH_CACHE[reach]


def _scene_window(name):
    """(start, end, resolution_m) parsed from a FIMBench scene folder name.

    Names carry their event window and resolution, e.g.
        HWM_20160928_20161009_780051W352232N   -> Hurricane Matthew, 10 m
        AI_20250412_854320W381510N             -> a single-date aerial scene
    A scene with no parsable date returns (None, None, res) and is only used when nothing else matches.
    """
    import re
    d = re.findall(r"_(\d{8})", name)
    # The resolution token (HWM_10_0m_, AI_0_2m_) lives in the BM FILENAME, never in the folder name. Parsing
    # the folder made every scene tie at inf, so "finest resolution wins" was dead code and the stable sort
    # silently degraded to alphabetical: the original bm[0] rule, merely gated. Callers pass the filename.
    r = re.search(r"_(\d+)_(\d+)m_", name)
    res = float("%s.%s" % (r.group(1), r.group(2))) if r else float("inf")
    if not d:
        return None, None, res
    s = d[0]
    e = d[1] if len(d) > 1 else d[0]
    return s, e, res


def _pick_benchmark(bhuc, bench_date, reach):
    """Pick the benchmark scene for THIS reach, not the first one glob happens to return.

    Three rules, in order, each of which this study has already been burned by:

      1. DATE. The scene's event window must contain bench_date. The Neuse folder holds both Hurricane
         Matthew (2016-09-28..10-09) and Hurricane Florence (2018-08-31..09-18); a glob that took the
         first hit could score Matthew's flood against Florence's benchmark.
      2. TIER. Tier_4 is a BLE synthetic 500-year design flood, not an observation of anything. It is
         refused outright, never silently globbed in.
      3. SPACE. The scene's raster must actually cover the reach. The Neuse Matthew event is split across
         two scenes; five of the eight Neuse reaches lie in the second one, and assigning them the first
         gave an empty intersection (no benchmark pixels, hence no score at all).

    Among the survivors, the finest resolution wins. Raises if nothing qualifies: an area with no valid
    benchmark must stop the run loudly, not score against the wrong flood.
    """
    import glob
    import rasterio
    from shapely.geometry import box as shp_box

    key = (bhuc, bench_date, str(reach))
    if key in _BM_CACHE:
        return _BM_CACHE[key]

    base = ROOT/"data"/"FIMBench"/bhuc
    scenes = sorted([d for d in glob.glob(str(base/"*")) if os.path.isdir(d)])
    line = _reach_ll(reach)
    cands = []
    for sd in scenes:
        name = os.path.basename(sd)
        if name.lower().startswith("tier_4") or "ble" in name.lower():
            continue                                              # rule 2: synthetic design flood, refused
        s, e, _ = _scene_window(name)
        bdc = bench_date.replace("-", "")
        if not s:
            # FAIL CLOSED. A dateless folder used to pass the date gate outright (the `if s and ...` short
            # circuit), and, tying at inf on resolution, could then win the alphabetical tie-break. That is
            # the Matthew-vs-Florence bug reinstated by a filename. Every FIMBench Tier_4 product
            # (BLE_100_<coords>) is dateless, so this is not hypothetical.
            continue
        if not (s <= bdc <= e):
            continue                                              # rule 1: wrong event
        clip = sorted(glob.glob(os.path.join(sd, "**", "*clip*.tif"), recursive=True))
        bms = clip or sorted(glob.glob(os.path.join(sd, "**", "*BM*.tif"), recursive=True))
        aois = sorted(glob.glob(os.path.join(sd, "**", "*AOI*.gpkg"), recursive=True))
        if not bms:
            continue
        try:                                                      # rule 3: must actually cover the reach
            with rasterio.open(bms[0]) as ds:
                import geopandas as gpd
                b = ds.bounds
                foot = gpd.GeoSeries([shp_box(b.left, b.bottom, b.right, b.top)],
                                     crs=ds.crs).to_crs(4326).iloc[0]
            if not foot.intersects(line):
                continue
        except Exception:
            continue
        _, _, res = _scene_window(os.path.basename(bms[0]))    # resolution lives in the FILENAME
        cands.append((res, bms[0], (aois[0] if aois else None), name))

    if not cands:
        raise SystemExit("no valid benchmark for reach %s (HUC %s, %s): none is date-matched, observed, "
                         "and spatially covering. Check the scene list under %s"
                         % (reach, bhuc, bench_date, base))
    cands.sort(key=lambda t: t[0])                                # finest resolution first
    res, bm, aoi, name = cands[0]
    out = ((str(Path(aoi).relative_to(ROOT)) if aoi else None), str(bm), name)
    _BM_CACHE[key] = out
    return out


def areas_df():
    """The 6-area config as a DataFrame, with the fields the dossier/plot functions expect
    (reach, fim_huc8, river, bench_date, stratum(=role), gup, gmid, gdn, gq, span_km, csi_ok, event, aoi_gpkg, bm_tif)."""
    rows = []
    for a in AREAS:
        huc = a["huc"].zfill(8); bd = a["bench_date"]
        bhuc = a.get("bench_huc", a["huc"]).zfill(8)      # benchmark HUC (differs from fim HUC for cross-HUC reaches)
        aoi_p, bm_p, ev = _pick_benchmark(bhuc, bd, a["reach"])
        aoi = [aoi_p] if aoi_p else []
        bm = [bm_p] if bm_p else []
        rows.append(dict(reach=a["reach"], fim_huc8=huc, huc8=huc, river=a["river"], bench_date=bd,
                         stratum=a["role"], dyn_class=a["dyn"], role=a["role"], gauge_paired=a["gauge_paired"],
                         gup=a["gup"], gmid=a["gdn"], gdn=a["gdn"], gq=a.get("gq", a["gdn"]), span_km=_gauge_span_km(a["gup"], a["gdn"]),
                         csi_ok=a["csi_ok"], fim_driver=a.get("fim_driver", "nwm"), event=ev,
                         aoi_gpkg=aoi_p,          # already ROOT-relative, straight from _pick_benchmark
                         bm_tif=bm_p))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = areas_df()
    pd.set_option("display.width", 200, "display.max_columns", 30)
    print(df[["reach", "river", "fim_huc8", "bench_date", "dyn_class", "role", "gauge_paired",
              "gup", "gdn", "csi_ok"]].to_string(index=False))
    df.to_csv(TAB/"study_areas_6.csv", index=False)
    print("\nwrote", TAB/"study_areas_6.csv")
