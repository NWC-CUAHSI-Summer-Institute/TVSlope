# 6-area study configuration: paths, study areas, slope treatments, gauge coordinates.
import os, glob
from pathlib import Path
from types import SimpleNamespace
import numpy as np, pandas as pd
def _repo_root():
    env = os.environ.get("SLOPE_ROOT")
    if env: return Path(env).expanduser().resolve()
    here = Path.cwd().resolve()
    for cand in (here, *here.parents):
        if (cand/".slope_root").exists() or (cand/"data").is_dir(): return cand
    return here
ROOT = _repo_root()
DATA = ROOT/"data"   # ROOT resolved portably at the top of this cell
SWORD = DATA/"SWORD_v17b_gpkg"/"na_sword_reaches_v17b.gpkg"
FT, CFS = 0.3048, 0.028316846592
EA = "EPSG:5070"
OUT  = ROOT/"output_final"
TAB, FIG, DOSS, PAP = OUT/"tables", OUT/"figures", OUT/"dossier", OUT/"paper"
for _d in (TAB, FIG, DOSS, PAP): _d.mkdir(parents=True, exist_ok=True)
AREAS = [
    dict(reach="74295200111", huc="10170203", river="Big Sioux River",  bench_date="2024-06-23",
         event="PSS_20240623T172530_962650W425825N",
         dyn="backwater", role="backwater",  gauge_paired=False, gup="06483950", gdn="06485500", gq="06483950", csi_ok=True, fim_driver="operational"),
    dict(reach="74295100321", huc="10230003", river="Little Sioux River", bench_date="2018-06-10",
         event="HWM_20180615_20180610_952917W425035N",
         dyn="kinematic", role="kinematic",  gauge_paired=False, gup=None,      gdn=None,      gq=None,      csi_ok=True, fim_driver="nwm"),
    dict(reach="74270100061", huc="07140105", river="Mississippi River", bench_date="2017-05-04", bench_huc="08010300",
         dyn="backwater", role="backwater",   gauge_paired=False, gup="07020850", gdn="07022000", gq="07022000", csi_ok=True, fim_driver="nwm"),
    # Ohio below McAlpine Dam = a gauge-paired reach (with Illinois 74282100101) -> the backwater time-varying S(Q) demo
    # (backwater, R2=0.99). 
    dict(reach="74267300251", huc="05140101", river="Ohio River",       bench_date="2025-04-12",
         dyn="backwater", role="backwater",   gauge_paired=True, gup="03293551", gdn="03294500", gq="03294500", csi_ok=True, fim_driver="operational"),
    dict(reach="74282100111", huc="07130011", river="Illinois River",   bench_date="2016-01-04",
         dyn="kinematic", role="kinematic",   gauge_paired=False, gup=None,       gdn="05585500", gq="05585500", csi_ok=True, fim_driver="nwm"),
    dict(reach="74282100101", huc="07130011", river="Illinois River",    bench_date="2016-01-04",
         dyn="kinematic", role="gauge-paired", gauge_paired=True,  gup="05586100", gdn="05586300", gq="05586100", csi_ok=True,  fim_driver="nwm"),
]

TREATMENTS  = ["baseline", "hfirissword_new", "swot_median", "swot_floodstage", "swot_maxwse", "gauge_timevarying"]
BASELINE    = "hfirissword_new"
TREAT_LABEL = {"baseline": "hydrofabric", "hfirissword_new": "IRIS-SWORD", "swot_median": "SWOT-median",
               "swot_floodstage": "SWOT-floodstage", "swot_maxwse": "SWOT-maxWSE",
               "gauge_timevarying": "gauge time-varying S(Q)"}
TREAT_COLOR = {"baseline": "#777777", "hfirissword_new": "#33bbee", "swot_median": "#0077bb",
               "swot_floodstage": "#ee3377", "swot_maxwse": "#ee7733", "gauge_timevarying": "#009988"}
DYN_COLOR   = {"kinematic": "#0077bb", "backwater": "#ee7733", "stable": "#999999"}
_gage = DATA/"paired_reach_SWOT_gage"/"gauge_latlon.csv"          # small bundled coord extract
if not _gage.exists(): _gage = DATA/"paired_reach_SWOT_gage"/"paired_reach_SWOT_gage.csv"   # full table fallback
_pg = pd.read_csv(_gage, usecols=["gage_id", "gage_name", "gage_latitude", "gage_longitude"],
                  dtype={"gage_id": str}, low_memory=False)
for _c in ["gage_latitude", "gage_longitude"]: _pg[_c] = pd.to_numeric(_pg[_c], errors="coerce")
GC = _pg.drop_duplicates("gage_id").set_index("gage_id")[["gage_name", "gage_latitude", "gage_longitude"]]
def _gauge_span_km(gup, gdn):
    try:
        if not gup or not gdn or gup not in GC.index or gdn not in GC.index: return 0.0
        la1, lo1 = float(GC.loc[gup, "gage_latitude"]), float(GC.loc[gup, "gage_longitude"])
        la2, lo2 = float(GC.loc[gdn, "gage_latitude"]), float(GC.loc[gdn, "gage_longitude"])
        r = 6371.0; p1, p2 = np.radians(la1), np.radians(la2); dphi = np.radians(la2-la1); dlmb = np.radians(lo2-lo1)
        h = np.sin(dphi/2)**2 + np.cos(p1)*np.cos(p2)*np.sin(dlmb/2)**2
        return float(2*r*np.arcsin(np.sqrt(h)))
    except Exception:
        return 0.0
def _pick_benchmark(bhuc):
    def _noclip(paths): return [p for p in paths if "clip" not in Path(p).name.lower()]
    bm = _noclip(sorted(glob.glob(str(ROOT/"data"/"FIMBench"/bhuc/"**"/"*BM*.tif"), recursive=True)))
    if not bm:
        bm = _noclip(sorted(glob.glob(str(ROOT/"data"/"FIMBench"/bhuc/"**"/"*.tif"), recursive=True)))
    return bm
def areas_df():
    rows = []
    for a in AREAS:
        huc = a["huc"].zfill(8); bd = a["bench_date"]
        bhuc = a.get("bench_huc", a["huc"]).zfill(8)
        evname = a.get("event")                                                # explicit FIMBench event subdir when the HUC holds several
        _base = ROOT/"data"/"FIMBench"/bhuc
        if evname:
            aoi = sorted(glob.glob(str(_base/evname/"*AOI*.gpkg")))
            bm  = [p for p in sorted(glob.glob(str(_base/evname/"*BM*.tif"))) if "clip" not in Path(p).name.lower()]
        else:
            aoi = sorted(glob.glob(str(_base/"**"/"*AOI*.gpkg"), recursive=True))
            bm  = _pick_benchmark(bhuc)                                         # FIX-1: full-res BM, never *clip*
        ev  = Path(aoi[0]).parent.name if aoi else (evname or "")
        rows.append(dict(reach=a["reach"], fim_huc8=huc, huc8=huc, river=a["river"], bench_date=bd,
                         fim_date=a.get("fim_date", bd),
                         stratum=a["role"], dyn_class=a["dyn"], role=a["role"], gauge_paired=a["gauge_paired"],
                         gup=a["gup"], gmid=a["gdn"], gdn=a["gdn"], gq=a.get("gq", a["gdn"]), span_km=_gauge_span_km(a["gup"], a["gdn"]),
                         csi_ok=a["csi_ok"], fim_driver=a.get("fim_driver", "nwm"), event=ev,
                         aoi_gpkg=(str(Path(aoi[0]).relative_to(ROOT)) if aoi else None),
                         bm_tif=(str(bm[0]) if bm else None)))
    return pd.DataFrame(rows)
CFG = SimpleNamespace(ROOT=ROOT, OUT=OUT, TAB=TAB, FIG=FIG, DOSS=DOSS, PAP=PAP, AREAS=AREAS, areas_df=areas_df,
                      TREATMENTS=TREATMENTS, BASELINE=BASELINE, TREAT_LABEL=TREAT_LABEL, TREAT_COLOR=TREAT_COLOR, DYN_COLOR=DYN_COLOR)
