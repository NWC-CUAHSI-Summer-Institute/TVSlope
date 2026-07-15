#!/usr/bin/env python3
# Fetch the large datasets that are NOT bundled in this repo (see README, "Data").
# Small derived tables (IRIS-SWORD slopes, SWOT slopes, gauge coordinates, bankfull, US states) ship in data/.
# This script downloads the two large sources the code needs: the FIMBench benchmark maps and the SWORD river network.
# USGS gauge series (discharge / stage) are fetched and cached automatically on the first notebook run (dataretrieval).
#
#   python get_data.py            # download FIMBench for the six study events + check for SWORD
#
import os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]   # repo root (this script lives in code/)
DATA = ROOT / "data"

# FIMBench benchmark events used by the study (benchmark HUC8, event date).
EVENTS = [
    ("10170203", "2024-06-23"),   # Big Sioux River
    ("10230003", "2018-06-10"),   # Little Sioux River
    ("08010300", "2017-05-04"),   # Mississippi River (benchmark HUC)
    ("05140101", "2025-04-12"),   # Ohio River below McAlpine Dam
    ("07130011", "2016-01-04"),   # Illinois River (two reaches, same HUC)
]

def get_fimbench():
    try:
        import fimeval
    except ImportError:
        print("fimeval not installed. Install it with:  pip install fimeval");  return
    out = DATA / "FIMBench"; out.mkdir(parents=True, exist_ok=True)
    for huc8, date in EVENTS:
        print(f"FIMBench: HUC {huc8}  {date} -> {out}")
        try:
            fimeval.benchFIMquery(huc8=huc8, event_date=date, download=True, out_dir=str(out))
        except Exception as e:
            print(f"  could not fetch HUC {huc8} {date}: {e}")

def check_sword():
    swd = DATA / "SWORD_v17b_gpkg" / "na_sword_reaches_v17b.gpkg"
    if swd.exists():
        print(f"SWORD present: {swd}"); return
    print("\nSWORD not found. Download the North America reaches GeoPackage and place it at:")
    print(f"    {swd}")
    print("  SWORD v17 (SWOT River Database, Altenau et al. 2021): https://doi.org/10.5281/zenodo.14727521")
    print("  Interactive browser / downloads:                      https://www.swordexplorer.com/")
    print("  (the file is na_sword_reaches_v17b.gpkg; rename the v17 reaches gpkg if needed)")

if __name__ == "__main__":
    get_fimbench()
    check_sword()
    print("\nUSGS gauge discharge/stage are downloaded and cached automatically on the first notebook run.")
    print("The staged HAND (data/fimbox_out) is rebuilt by the notebook when REGEN_FIM=1 (needs fimbox installed).")
