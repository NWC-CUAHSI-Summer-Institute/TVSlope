# Evaluating the Sensitivity of HAND Flood Inundation Mapping to River Slope

### Time-Varying River Slope in Operational HAND Flood Inundation Mapping

**CUAHSI Summer Institute 2026** · Innovation in Flood Inundation Mapping for Operational Forecasting

![Status](https://img.shields.io/badge/status-active-2ea44f?style=flat-square)
![Institute](https://img.shields.io/badge/CUAHSI-Summer_Institute_2026-2166ac?style=flat-square)
![Compute](https://img.shields.io/badge/compute-CIROH_JupyterHub-e08214?style=flat-square)
![Reaches](https://img.shields.io/badge/study_reaches-69-9b59b6?style=flat-square)
![Treatments](https://img.shields.io/badge/slope_treatments-5-b2182b?style=flat-square)


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
USGS gauge series download an cache automatically on the first run.

## Data

**Provided in `data/` (you do not download).**

| File | What it is | Provenance |
| --- | --- | --- |
| `data/slope_treatments.csv` | Per-reach slope for each treatment (hydrofabric, IRIS-SWORD, SWOT median/floodstage/maxWSE) | Derived in this study |
| `data/FIMHF_IRIS_new.csv`, `data/FIMHF_IRIS_v1.0.csv` | IRIS-SWORD static slope | Built from **IRIS v3.3** + **SWORD v17b**, following Chen et al. (2025) |
| `data/paired_reach_SWOT_gage/gauge_latlon.csv` | USGS gauge coordinates (id, name, lat, lon) | USGS NWIS |
| `data/study_area_gauges.csv` | Same-river upstream/on-reach/downstream gauge triplets per reach | Derived in this study |
| `data/fimbox_bankfull_2yr_cms.parquet` | 2-year recurrence (bankfull) discharge per NWM feature_id | NWM recurrence flows |
| `data/us_states.gpkg` | US state boundaries for the CONUS map | Public US state boundaries |

**Fetched by code — not in the repo. Run `python get_data.py`.**

| Data | How to get it | Source |
| --- | --- | --- |
| FIMBench benchmark flood maps (`data/FIMBench/`) | `python get_data.py` (uses `fimeval`) | **FIMbench** (https://tethys.ciroh.org/apps/fimbench-gui/) |
| SWORD v17b river network (`data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg`) | `python get_data.py` | **SWORD v17** (https://zenodo.org/records/15299138) |
| USGS gauge discharge & stage (`data/discharge/`, `data/twin_gauge/`) | cached on the first notebook run (`dataretrieval`) | USGS NWIS |
| NWM hydrofabric + 3DEP DEM + staged HAND (`data/fimbox_out/`) | Rebuilt by the notebook when `REGEN_FIM=1` (needs `fimbox`) | NWM / USGS 3DEP, via FIMbox |

### Citations

- **IRIS v3.3** (ICESat-2 River Surface Slope) — Scherer, D., Schwatke, C., Dettmering, D., & Seitz, F. (2022).
  ICESat-2 based River Surface Slope and Its Impact on Water Level Time Series From Satellite Altimetry.
  *Water Resources Research.* https://doi.org/10.1029/2022WR032842 · data: https://zenodo.org/records/14616464
- **SWORD v17b** (SWOT River Database) — Elizabeth H. Altenau, Tamlin M. Pavelsky, Michael T. Durand, Xiao Yang, Renato P. d. M. Frasson& Liam Bendezu. (2025). SWOT River Database (SWORD) (Version v17b) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.15299138 · data: [https://doi.org/10.5281/zenodo.14727521 · https://www.swordexplorer.com/](https://zenodo.org/records/15299138)
- **IRIS-SWORD slope** — Chen, Y., Cohen, S., Baruah, A., Devi, D., Dhital, S., Tian, D., & Munasinghe, D. (2025). Merging Remote Sensing Derived River Slope Datasets with High-Resolution Hydrofabrics for the United States. Scientific Data, 12(1), 1657.
- **National Water Model** (retrospective + operational short-range forecast) — NOAA Office of Water Prediction.
- **USGS** gauge data and **3DEP** 10 m DEM — U.S. Geological Survey.
- **FIMBench** benchmark flood maps — Surface Dynamics Modeling Lab, University of Alabama.

## Code and copyright


| Path | Origin | What we changed |
| --- | --- | --- |
| `code/tvslope_src/engine/*.py` | Our own code | Written for this study. `timevarying_slope.py` adapts the TimeVariantSlope `S(Q)` method; `fim_reach.py` and `fim_eval.py` reimplement the RiverJoin river-matching and FIMeval scoring concepts. |
| `code/tvslope_src/fimbox_ext/*.py` | **Built on FIMbox** ([github.com/sdmlua/fimbox](https://github.com/sdmlua/fimbox)) | We modified the code from FIMbox: observation-calibration disabled, per-treatment slope injection, a branch-0 tributary gap-filler, and NWM-forecast forcing. Each file carries a `Built on FIMbox` header noting the source and the change. |

### Source tools and licenses

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
---
---

## Team

| Name | Institution | GitHub |
|---|---|---|
| Zih-Syun Chen | University of Houston | [@zixunn](https://github.com/zixunn) |
| Sebastian Marshall | Johns Hopkins University | [@rushmarshall](https://github.com/rushmarshall) |
| Pitamber Wagle | Brigham Young University | [@Pitamberwagle](https://github.com/Pitamberwagle) |
| Reza Jamshidi | Northeastern University | [@Reza-Jamshidi](https://github.com/Reza-Jamshidi) |


**Theme leads:** Sagy Cohen and Anupal Baruah, University of Alabama

---
<div align="center">

**CUAHSI Summer Institute 2026** &nbsp;·&nbsp; **Team Slippery Slope**

University of Houston &nbsp;·&nbsp; Johns Hopkins University &nbsp;·&nbsp; Brigham Young University &nbsp;·&nbsp; Northeastern University 

</div>

