"""Stage the data tree `code/07_sebastian_sq_study.ipynb` expects, so it runs on this machine instead of Zixun's.

The notebook and `tvslope_src/sebastian/*.py` hard-code

    ROOT = Path("/Users/zixun/2026SI/slipperyslope")

and every input hangs off it, so cell 3 dies immediately on any other machine. Nothing in the science needs
that path; it is only where his files happen to live. This builds the same tree here, SYMLINKED to data that
already exists on this machine, so no gigabyte is copied twice.

What the tree must contain, read straight out of the source:

  data/paired_reach_SWOT_gage/paired_reach_SWOT_gage.csv   per_reach3.py:32, read AT IMPORT
  data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg          per_reach3.py:21, fim_eval.py:23
  data/FIMBench/<bench_huc>/**/{*_BM.tif,*_AOI.gpkg}       final_config.py:87-91
  data/fimbox_out/HUC<huc>/fim-outputs/*.tif               fim_reach.py:35, the FIM extents cell 44 scores
  data/discharge/, data/twin_gauge/                        NWIS caches; per_reach3 downloads what is missing
  output_exp6/reach3/reach3_selected.csv                   per_reach3.py:36, read AT IMPORT
  output_exp6/per_reach3/, output_final/                   output dirs
  code/                                                    on sys.path; the src modules

Everything staged here is REAL data already fetched from the operational sources:
  FIMBench benchmarks   sdmlua fimeval.benchFIMquery
  flood extents         NOAA-OWP inundation-mapping (v4.9.16.0), driven on the OWP HAND 4.9.9.0 cache
  SWOT-gage pairing     Harlan et al. 2026, USGS ScienceBase 10.5066/P1FE9W9E

Author: Sebastian R.O. Marshall
"""
import json
import os
import sys
import shutil
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parent
ROOT = REPO / "slipperyslope"                      # the local stand-in for /Users/zixun/2026SI/slipperyslope
PROJ = Path("/Users/sebastianmarshall/dev/swot-fim-2026/local_data/proj_mirror")  # local mirror; never the author's project tree
RUN = Path("/Users/sebastianmarshall/dev/swot-fim-2026/local_data/run")
sys.path.insert(0, str(REPO / "src"))


def link(src, dst):
    """Symlink src -> dst, replacing a stale link. Never copies: the benchmarks alone are ~2 GB."""
    src, dst = Path(src), Path(dst)
    if not src.exists():
        return f"MISSING SOURCE {src}"
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_symlink() or dst.exists():
        if dst.is_symlink():
            dst.unlink()
        elif dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    os.symlink(src, dst)
    return "linked"


print("=" * 96)
print(f"STAGING {ROOT}")
print("=" * 96)

# ---- code/ on sys.path -------------------------------------------------------------------------------
print(f"  code/                      {link(REPO / 'src', ROOT / 'code')}")

# ---- the two files per_reach3 reads AT IMPORT --------------------------------------------------------
print(f"  paired_reach_SWOT_gage     "
      f"{link(PROJ / 'USGS_Gauges_Approach/data/sciencebase_swot_gage/paired_reach_SWOT_gage.csv', ROOT / 'data/paired_reach_SWOT_gage/paired_reach_SWOT_gage.csv')}")

sword = PROJ / "03_Data/incoming/sword_v17b/gpkg/na_sword_reaches_v17b.gpkg"
print(f"  SWORD v17b                 {link(sword, ROOT / 'data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg')}")

# ---- FIMBench benchmarks, one dir per benchmark HUC ---------------------------------------------------
BENCH_HUCS = ["05140101", "07130011", "08010300", "12020003"]
for h in BENCH_HUCS:
    print(f"  FIMBench/{h}         {link(RUN / f'bench_{h}', ROOT / 'data/FIMBench' / h)}")

# ---- the flood extents cell 44 scores ---------------------------------------------------------------
# fim_reach.py puts them under data/fimbox_out/HUC<huc>/fim-outputs/. Ours were produced by the NOAA-OWP
# engine on the OWP HAND cache, so they are the operational product, not a fimbox self-derived HAND.
ext_json = PROJ / "06_Results/results/fim_rebuild_extents.json"
if ext_json.exists():
    ext = json.loads(ext_json.read_text())
    reg = pd.read_csv(PROJ / "06_Results/results/fim_rebuild_registry.csv",
                      dtype={"reach": str, "fim_huc": str})
    huc_of = dict(zip(reg.reach, reg.fim_huc))
    n = 0
    for reach, treats in ext.items():
        huc = huc_of.get(reach)
        if not huc:
            continue
        fb = ROOT / "data/fimbox_out" / f"HUC{huc}" / "fim-outputs"
        fb.mkdir(parents=True, exist_ok=True)
        for t, p in treats.items():
            # name them so both the notebook and a human can tell what they are
            tag = t.replace(" ", "_")
            dst = fb / f"reach{reach}_{tag}.tif"
            if dst.is_symlink() or dst.exists():
                dst.unlink()
            os.symlink(p, dst)
            n += 1
    print(f"  fimbox_out/                linked {n} flood extents (NOAA-OWP inundation-mapping)")
else:
    print("  fimbox_out/                NO EXTENTS YET (run fim_rebuild/gen_fim.py first)")

# ---- the AOI tree fim_reach._aoi_dir(huc) looks for --------------------------------------------------
# It wants HUC<huc>/watershed-data/. The OWP HAND cache IS that tree: it carries branches/*/hydroTable_*.csv
# (the synthetic rating curves cells 28 and 40 read) and nwm_subset_streams.gpkg. Linking it means those
# cells read the OPERATIONAL rating curves, not a fimbox self-derived HAND.
import final_config as _CFG
for _h in sorted({str(x).zfill(8) for x in _CFG.areas_df().fim_huc8}):
    _src = RUN / "output" / f"flood_{_h}" / _h
    _dst = ROOT / "data" / "fimbox_out" / f"HUC{_h}" / "watershed-data"
    print(f"  HUC{_h}/watershed-data     {link(_src, _dst)}")

# ---- the canonical slope table cells 15 and 40 read --------------------------------------------------
print(f"  slope_treatments.csv       "
      f"{link(PROJ / 'USGS_Gauges_Approach/data/tvslope/slope_treatments.csv', ROOT / 'output_exp6/select/slope_treatments.csv')}")

# ---- output dirs and the NWIS caches per_reach3 fills on demand ---------------------------------------
for d in ("output_final", "output_exp6/per_reach3", "output_exp6/reach3",
          "data/discharge", "data/twin_gauge"):
    (ROOT / d).mkdir(parents=True, exist_ok=True)
print("  output dirs + NWIS caches  created")

# ---- reach3_selected.csv: the study-reach table per_reach3 reads AT IMPORT ----------------------------
# Built from final_config.AREAS, which is the notebook's own study design. gmid is the on-reach gauge.
sel = ROOT / "output_exp6/reach3/reach3_selected.csv"
if not sel.exists():
    rows = [
        dict(reach="75120400053", river="Neches River",      gup="08040600", gmid="08041000",
             gdn="08041000", gq="08041000", span_km=48.7),
        dict(reach="74282100101", river="Illinois River",    gup="05586100", gmid="05586100",
             gdn="05586300", gq="05586100", span_km=30.0),
        dict(reach="74270100061", river="Mississippi River", gup="07020850", gmid="07022000",
             gdn="07022000", gq="07022000", span_km=40.0),
        dict(reach="74267300251", river="Ohio River",        gup="03293551", gmid="03294500",
             gdn="03294500", gq="03294500", span_km=10.3),
        dict(reach="74282100111", river="Illinois River",    gup="05585500", gmid="05585500",
             gdn="05585500", gq="05585500", span_km=19.7),
        dict(reach="75120400151", river="Neches River",      gup="08040600", gmid="08040600",
             gdn="08040600", gq="08040600", span_km=9.4),
    ]
    pd.DataFrame(rows).to_csv(sel, index=False)
    print(f"  reach3_selected.csv        built ({len(rows)} study reaches, from final_config.AREAS)")
else:
    print("  reach3_selected.csv        already present")

# ---- us_states.gpkg (optional; only used for context maps) -------------------------------------------
cand = list(PROJ.glob("**/us_states.gpkg")) + list(PROJ.glob("**/cb_*_state_*.gpkg"))
if cand:
    print(f"  us_states.gpkg             {link(cand[0], ROOT / 'data/us_states.gpkg')}")
else:
    print("  us_states.gpkg             not found (only used for context maps)")

print("\nSTAGED. Point the notebook at:")
print(f"  ROOT = Path({str(ROOT)!r})")
