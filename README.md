# Evaluating the Sensitivity of HAND Flood Inundation Mapping to River Slope

The uncalibrated NOAA-OWP HAND synthetic rating curve is Manning (`Q ∝ √S`), so the river **slope** `S` is a
first-order control on the mapped flood extent. This repository asks whether replacing that slope with a
static-satellite product (IRIS-SWORD, SWOT) or a **time-varying gauge-derived `S(Q)`** measurably changes HAND-FIM
skill, and where (by hydraulic regime) it matters. One notebook runs the whole study end to end over six reaches
and scores every slope treatment against FIMBench.

## What's here

```
code/TV_Slope_FIM.ipynb        the study notebook (run this)
code/tvslope_src/engine/       analysis modules 
code/tvslope_src/fimbox_ext/   build HAND + generate the FIM
data/                          small derived data
get_data.py                    downloads the large datasets that are not provided (FIMBench, SWORD)
```

## Run it

```bash
conda env create -f environment.yml && conda activate slope   # geopandas, rasterio, dataretrieval, ...
python get_data.py                                             # FIMBench + SWORD (large; not in the repo)
TV_Slope_FIM.ipynb
```
USGS gauge series download and
cache automatically on the first run.

## Data

**Bundled in `data/` — small derived tables, already in the repo (you do not download these).**

| File | What it is | Provenance |
| --- | --- | --- |
| `data/slope_treatments.csv` | Per-reach slope for each treatment (hydrofabric, IRIS-SWORD, SWOT median/floodstage/maxWSE) | Derived in this study |
| `data/FIMHF_IRIS_new.csv`, `data/FIMHF_IRIS_v1.0.csv` | IRIS-SWORD static channel slope per reach | Built from **IRIS v3.3** (ICESat-2 river slope) + **SWORD v17b**, following Chen et al. (2025) |
| `data/paired_reach_SWOT_gage/gauge_latlon.csv` | USGS gauge coordinates (id, name, lat, lon) | USGS NWIS (small extract of the full paired table) |
| `data/study_area_gauges.csv` | Same-river upstream/on-reach/downstream gauge triplets per reach | Derived in this study |
| `data/fimbox_bankfull_2yr_cms.parquet` | 2-year recurrence (bankfull) discharge per NWM feature_id | NWM recurrence flows |
| `data/us_states.gpkg` | US state boundaries for the CONUS context map | Public US state boundaries |

**Fetched by code — large datasets, not in the repo. Run `python get_data.py`.**

| Data | How to get it | Source |
| --- | --- | --- |
| FIMBench benchmark flood maps (`data/FIMBench/`) | `python get_data.py` (uses `fimeval`) | SDML **FIMbench** |
| SWORD v17b river network (`data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg`) | `python get_data.py` prints the download link; place the GeoPackage in that folder | **SWORD v17**, Zenodo / swordexplorer |
| USGS gauge discharge & stage (`data/discharge/`, `data/twin_gauge/`) | Automatic — cached on the first notebook run (`dataretrieval`) | USGS NWIS |
| NWM hydrofabric + 3DEP DEM + staged HAND (`data/fimbox_out/`) | Rebuilt by the notebook when `REGEN_FIM=1` (needs `fimbox`) | NWM / USGS 3DEP, via FIMbox |

### Data citations

- **IRIS v3.3** (ICESat-2 River Surface Slope) — Scherer, D., Schwatke, C., Dettmering, D., & Seitz, F. (2022).
  ICESat-2 based River Surface Slope and Its Impact on Water Level Time Series From Satellite Altimetry.
  *Water Resources Research.* https://doi.org/10.1029/2022WR032842 · data: https://zenodo.org/records/14616464
- **SWORD v17b** (SWOT River Database) — Altenau, E. H., et al. (2021). The SWOT Mission River Database (SWORD):
  A Global River Network for Satellite Data Products. *Water Resources Research.*
  https://doi.org/10.1029/2021WR030054 · data: https://doi.org/10.5281/zenodo.14727521 · https://www.swordexplorer.com/
- **IRIS-SWORD combined static slope** — Chen et al. (2025), *Scientific Data.*
- **National Water Model** (retrospective + operational short-range forecast) — NOAA Office of Water Prediction.
- **USGS NWIS** gauge data and **3DEP** 10 m DEM — U.S. Geological Survey.
- **FIMBench** benchmark flood maps — Surface Dynamics Modeling Lab, University of Alabama.

## Source code and copyright


| Path | Origin | What we changed |
| --- | --- | --- |
| `code/tvslope_src/engine/*.py` | Our own code | Written for this study. `timevarying_slope.py` adapts the TimeVariantSlope `S(Q)` method; `fim_reach.py` and `fim_eval.py` reimplement the RiverJoin river-matching and FIMeval scoring concepts. |
| `code/tvslope_src/fimbox_ext/*.py` | **Built on FIMbox** (github.com/sdmlua/fimbox) | Our drivers wrap FIMbox: observation-calibration disabled, per-treatment slope injection, a branch-0 tributary gap-filler, and NWM-forecast forcing. Each file carries a `Built on FIMbox` header noting the source and the change. |
| FIMbox engine (not vendored) | github.com/sdmlua/fimbox | Called from source, **unmodified**; installed separately. |
| NOAA-OWP/inundation-mapping (not vendored) | github.com/NOAA-OWP/inundation-mapping | The HAND-FIM method FIMbox implements; not modified. |

### Upstream tools and licenses

| Tool | Owner | License | Repository |
| --- | --- | --- | --- |
| FIMbox | Surface Dynamics Modeling Lab (Univ. of Alabama) | GPL-3.0 | https://github.com/sdmlua/fimbox |
| FIMserv | SDML | see repo | https://github.com/sdmlua/FIMserv |
| FIMeval | SDML | see repo | https://github.com/sdmlua/fimeval |
| FIMbench | SDML | see repo | https://github.com/sdmlua/fimbench |
| RiverJoin | SDML | see repo | https://github.com/sdmlua/riverjoin_py |
| NOAA-OWP/inundation-mapping | NOAA Office of Water Prediction | see repo | https://github.com/NOAA-OWP/inundation-mapping |

> **License note.** FIMbox is **GPL-3.0**. Because the drivers in `code/tvslope_src/fimbox_ext/` build on FIMbox,
> they are likewise distributed under **GPL-3.0**. Add a top-level `LICENSE` file before publishing more widely.

Study code © Zih-Syun Chen. Upstream tools and datasets belong to their respective authors.
