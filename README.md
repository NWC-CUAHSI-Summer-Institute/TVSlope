<div align="center">

  # Evaluating the Sensitivity of HAND Flood Inundation Mapping to River Slope

### Innovation in Flood Inundation Mapping for Operational Forecasting

**CUAHSI Summer Institute 2026** · 
![Status](https://img.shields.io/badge/status-active-2ea44f?style=flat-square)
![Institute](https://img.shields.io/badge/CUAHSI-Summer_Institute_2026-2166ac?style=flat-square)
![Reaches](https://img.shields.io/badge/study_reaches-6-9b59b6?style=flat-square)
![Treatments](https://img.shields.io/badge/slope_treatments-4-b2182b?style=flat-square)
![Python](https://img.shields.io/badge/python-3.10-3776AB?style=flat-square&logo=python&logoColor=white)

The uncalibrated NOAA-OWP HAND synthetic rating curve is Manning (`Q ∝ √S`), so the river **slope** `S` is an
important control on the mapped flood extent. This repository asks whether replacing that slope with a
static-satellite product (IRIS-SWORD, SWOT) or a **time-varying gauge-derived `S(Q)`** measurably changes HAND-FIM
skill, and where (by hydraulic regime) it matters.

</div>

<p align="center"><img src="output_final/figures/workflow_architecture.png" width="88%" alt="workflow"></p>

---

## Overview

Operational OWP **HAND** flood-inundation mapping (FIM) turns National Water Model (NWM) discharge into flood
extent through a Manning **synthetic rating curve (SRC)**. Because the uncalibrated SRC is Manning
(*Q* &propto; &radic;*S*), the river **slope** *S* is a first-order control on the rating curve. This repository
evaluates, end to end and against the **FIMBench** benchmark, whether a better slope makes a better flood map:
a **static-satellite** baseline (IRIS-SWORD; Chen et al., 2025), three **SWOT**-derived slopes, and a new
**time-varying gauge slope** *S(Q)* fitted from two paired gauges and injected into the rating curve by iterating
*Q* = *Q*<sub>0</sub>&radic;(*S(Q)*/*S*<sub>0</sub>).

**Headline finding.** Across six SWOT-observed reaches, the slope source (and even its flow dependence) is a
**second-order** control on flood extent, while the **hydraulic regime** — free-flowing (kinematic) versus backwater
— is **first-order**: an order-of-magnitude slope range collapses to a few-hundredths range in CSI.

## What's here

```
code/TV_Slope_FIM.ipynb        the consolidated study notebook (run this)
code/work6_3DHRS.ipynb         the focused six-reach study and manuscript figures
code/timevary_slope.ipynb      the time-varying gauge S(Q) method over the full reach selection
code/study_area.ipynb          FIM reach selection (FIMBench coverage + gauge triplets)
code/gauge_study.ipynb         CONUS-wide gauge-availability survey (gauges only, not FIM)
code/swot_geoid_slope.ipynb    vertical datum: SWOT WSE on the geoid, and slope's datum sensitivity
code/tvslope_src/engine/       analysis modules
code/tvslope_src/fimbox_ext/   build HAND + generate the FIM
code/get_data.py               downloads the large datasets that are not provided (FIMBench, SWORD)
notebooks/work_0607.ipynb      Sebastian's parallel S(Q) notebook  (see README_SEBASTIAN.md)
notebooks/sq_core.py           the S(Q) chain rebuilt against the public USGS NWIS API
src/                           the modules that notebooks/work_0607.ipynb imports
data/                          small derived data
output_final/                  figures and tables written by the notebooks
```

## Notebooks

The first two notebooks are **reach-selection** steps; the rest are the **FIM analysis**.

| Notebook | Scope | What it does |
|---|---|---|
| [`code/gauge_study.ipynb`](code/gauge_study.ipynb) | **Gauges only — not FIM** | A standalone survey of USGS gauge availability across the entire CONUS SWORD network: which reaches carry a same-river upstream/on-reach/downstream gauge triplet that can form a water-surface slope. Independent of flood-inundation mapping and FIMBench. |
| [`code/study_area.ipynb`](code/study_area.ipynb) | **FIM reach selection** | Selects the reaches used in the FIM study: those covered by a **FIMBench** benchmark (**Tier 1–3** or high-water-mark) **and** carrying a usable gauge triplet, so both the benchmark and the paired-gauge slope are available. Benchmarks are auto-downloaded via `fimeval`. |
| [`code/timevary_slope.ipynb`](code/timevary_slope.ipynb) | FIM method | Develops the time-varying gauge *S(Q)* method over the full reach selection: paired-gauge slope vs discharge, iterative Manning injection, HAND-FIM, and River-Mask CSI/F1. |
| [`code/work6_3DHRS.ipynb`](code/work6_3DHRS.ipynb) | FIM headline study | The focused six-reach study and manuscript figures: static-satellite vs gauge time-varying *S(Q)*, scored on the River-Mask domain, with Results & Discussion. |
| [`code/TV_Slope_FIM.ipynb`](code/TV_Slope_FIM.ipynb) | Consolidated study | Runs the whole study end to end over the six reaches and scores every slope treatment against FIMBench. |
| [`code/swot_geoid_slope.ipynb`](code/swot_geoid_slope.ipynb) | **Vertical datum** | Verifies which vertical datum SWOT WSE is on, and quantifies how much the choice of geoid (ellipsoid / EGM2008 / EGM96 / NAVD88) changes a computed water-surface slope. See [Vertical datum](#vertical-datum-swot-wse-and-the-geoid). |
| [`notebooks/work_0607.ipynb`](notebooks/work_0607.ipynb) | Parallel S(Q) reading | Sebastian's working notebook — a separate reading of the same research question over 17 reaches. Documented in [`README_SEBASTIAN.md`](README_SEBASTIAN.md). ~74 MB with embedded outputs; open it locally. |

## Installation

```bash
git clone https://github.com/NWC-CUAHSI-Summer-Institute/TVSlope.git
cd TVSlope
conda env create -f environment.yml     # base geo-stack: geopandas, rasterio, pyproj, scipy, matplotlib, ...
conda activate slope
python code/get_data.py                 # FIMBench + SWORD (large; not in the repo)
```

The notebooks also use three HAND-FIM tools from the [SDML lab](https://github.com/sdmlua). Install the ones you
need:

```bash
pip install fimeval        # query + download FIMBench benchmarks  (needed by study_area / timevary)
pip install fimserve       # HAND-FIM staging and serving          (needed to (re)generate FIM)
pip install "git+https://github.com/sdmlua/fimbox"   # HAND-FIM generation (needed to (re)generate FIM)
```

| To do this | You need |
|---|---|
| Reproduce the cached figures (`work6_3DHRS`) | base env only |
| Run the vertical-datum notebook (`swot_geoid_slope`) | base env only (downloads geoid grids on first use) |
| Select reaches / download benchmarks (`gauge_study`, `study_area`) | base env + `fimeval` |
| Regenerate FIM from scratch (`REGEN_FIM=True` / `TVS_REGEN=1`) | base env + `fimeval` + `fimbox` + `fimserve` |

## Quick start

```bash
# reproduce the flagship six-reach study end to end (uses the cached FIM extents)
jupyter nbconvert --to notebook --execute --inplace code/work6_3DHRS.ipynb
```

The core method in a few lines (as inlined in the notebook):

```python
# 1. fit a non-linear slope-discharge relation S(Q) from two paired gauges
fit = fit_sq(discharge_cms, water_surface_slope)          # power-law or quadratic, whichever fits better
# 2. inject it into every HAND hydro-table row by iterating Q = Q0 * sqrt(S(Q)/S0)
Q_new, S_new = solve_Q(Q0, S0, fit["func"])               # a time-varying synthetic rating curve
# 3. run FIMbox to a flood extent and score it against FIMBench on the river-mask domain
csi = score_rm(fim_tif, benchmark_tif, river_mask(aoi, reach))["CSI"]
```

Running `work6_3DHRS.ipynb` writes every figure into [`output_final/`](output_final/), for example:

<p align="center">
  <img src="output_final/figures/sq_relationship.png" width="49%" alt="S(Q)">
  <img src="output_final/figures/src_all_reaches.png" width="49%" alt="rating curves">
</p>

## Method &amp; workflow

![Workflow](figure/workflow.png)

Two choices make the comparison defensible: **(1)** every event is forced by one NWM family (retrospective, or the
operational short-range forecast for post-2023 floods — never a substituted gauge); **(2)** every metric is computed
on the **river mask** (the union of the reach's NWM catchments, benchmark cleaned to its largest connected
component), removing the large off-channel false-negative term that a whole-benchmark score would impose.

## Vertical datum: SWOT WSE and the geoid

A slope is a difference of heights over a distance, so a **constant** offset between vertical datums cancels
and the datum looks like bookkeeping. The **gradient** of the datum separation does not cancel — and on these
reaches it is the same order of magnitude as the river slope itself. [`code/swot_geoid_slope.ipynb`](code/swot_geoid_slope.ipynb)
works this out; [`code/tvslope_src/engine/datum.py`](code/tvslope_src/engine/datum.py) is the module.

<p align="center"><img src="output_final/figures/geoid_datum_slope.png" width="94%" alt="vertical datum and slope"></p>

**1 · SWOT WSE is already on the geoid — do not "convert" it.** SWOT L2_HR_RiverSP delivers `wse` referenced
to **EGM2008**, not to the WGS84 ellipsoid. We test this rather than quote it: scored against SWORD/MERIT
(moved onto EGM2008 first), treating `wse` as orthometric leaves a median residual of **+0.41 m**, while
treating it as ellipsoidal leaves **+29.23 m**. Subtracting a geoid undulation from `wse` is therefore a
**~30 m blunder**, not a refinement. `datum.SWOT_WSE_DATUM` records the datum and `verify_swot_datum()`
re-checks it on any new pull.

**2 · The geoid's along-channel gradient is a first-order slope term.** Writing a slope from ellipsoidal
heights, `dh/dx = dH/dx + dN/dx` — the river slope you want, plus a geoid gradient you did not ask for.
Over the 92 SWOT-observed study reaches (median length 10.0 km):

| Quantity | median | p90 | max |
|---|---:|---:|---:|
| along-channel geoid gradient &#124;dN/dx&#124; (EGM2008) | 4.1 mm/km | 16.2 | **32.9** |
| EGM2008 − EGM96 slope difference | 1.2 mm/km | 6.2 | **13.0** |
| river water-surface slope &#124;S&#124; *(70 reaches above 10 mm/km)* | 135 mm/km | 255 | 409 |

On **21 of those 70** reaches the geoid gradient is worth more than 10 % of the river slope, on **3** more than
half, and on **8 of 92** it exceeds **17 mm/km** — SWOT's own reach-slope accuracy requirement — all by itself.
A worked example in the notebook (Arkansas River, 10.8 km) computes the same reach at 158 mm/km on EGM96 and
134 mm/km on the ellipsoid: a **24 mm/km**, ~15 % error. Since the uncalibrated SRC is Manning (*Q* &propto; &radic;*S*),
a 10 % slope error moves discharge ~5 % at fixed stage — and it does so with a spatial pattern that looks like
real topography, which is exactly the kind of error that survives visual inspection. **A slope computed on the
wrong datum mimics the geoid, not the river bed.**

**3 · The datasets here do not share a geoid.** SWOT `wse` is **EGM2008**, SWORD/MERIT Hydro `wse` is
**EGM96**, IRIS is **EIGEN-6C4**, and USGS gauge `alt_va` is **NAVD88**. Differencing across two models injects
the difference between them into the slope. Put every source on one model with `datum.convert_geoid()` before
differencing; the slope treatments in `data/slope_treatments.csv` are internally consistent, and this notebook
is the check that keeps them that way.

## Data

The repository commits only the small derived tables that cannot be queried from a public service; everything else
is downloaded or generated by the workflow (full manifest, sizes, and sources in [`DATA.md`](DATA.md)).

**Provided in `data/`**

| File | What it is | Provenance |
| --- | --- | --- |
| `data/slope_treatments.csv` | Per-reach slope for each treatment (hydrofabric, IRIS-SWORD, SWOT median/floodstage/maxWSE) | Derived in this study |
| `data/FIMHF_IRIS_new.csv`, `data/FIMHF_IRIS_v1.0.csv` | IRIS-SWORD static slope | Built from **IRIS v3.3** + **SWORD v17b**, following Chen et al. (2025) |
| `data/paired_reach_SWOT_gage/gauge_latlon.csv` | USGS gauge coordinates (id, name, lat, lon) | USGS NWIS |
| `data/study_area_gauges.csv` | Same-river upstream/on-reach/downstream gauge triplets per reach | Derived in this study |
| `data/fimbox_bankfull_2yr_cms.parquet` | 2-year recurrence (bankfull) discharge per NWM feature_id | NWM recurrence flows |
| `data/us_states.gpkg` | US state boundaries for the CONUS map | Public US state boundaries |
| `data/swot_hydrocron_study_reaches.csv` | SWOT L2_HR_RiverSP reach observations (WSE, slope, width, quality) for the study reaches | **Hydrocron** API (PO.DAAC) |
| `data/swot_study_reach_nodes.csv` | SWORD node chain (coordinates, `dist_out`, WSE) for those reaches — lets the datum notebook run without the 3.7 GB SWORD download | **SWORD v17b** |
| `data/swot_study_reaches_sword.csv` | SWORD reach centroids, WSE and slope for those reaches | **SWORD v17b** |

**Fetched by code — run `python code/get_data.py`.**

| Data | How to get it | Source |
| --- | --- | --- |
| FIMBench benchmark flood maps (`data/FIMBench/`) | `python code/get_data.py` (uses `fimeval`) | **FIMbench** (https://tethys.ciroh.org/apps/fimbench-gui/) |
| SWORD v17b river network (`data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg`) | `python code/get_data.py` | **SWORD v17** (https://zenodo.org/records/15299138) |
| USGS gauge discharge & stage (`data/discharge/`, `data/twin_gauge/`) | cached on the first notebook run (`dataretrieval`) | USGS NWIS |
| NWM hydrofabric + 3DEP DEM + staged HAND (`data/fimbox_out/`) | Rebuilt by the notebook when `REGEN_FIM=1` (needs `fimbox`) | NWM / USGS 3DEP, via FIMbox |

## Examples

<table>
<tr>
<td width="50%"><img src="output_final/figures/aoi_maps_2x3.png" alt="study reaches"><br><sub><b>Six study reaches</b> — SWOT reach, FIMBench flood extent, river-mask evaluation domain.</sub></td>
<td width="50%"><img src="output_final/figures/csi_f1_per_reach.png" alt="skill"><br><sub><b>Flood-map skill (CSI, F1)</b> by slope treatment on the river-mask domain.</sub></td>
</tr>
</table>

## Citations

- **IRIS v3.3** (ICESat-2 River Surface Slope) — Scherer, D., Schwatke, C., Dettmering, D., & Seitz, F. (2022).
  ICESat-2 based River Surface Slope and Its Impact on Water Level Time Series From Satellite Altimetry.
  *Water Resources Research.* https://doi.org/10.1029/2022WR032842 · data: https://zenodo.org/records/14616464
- **SWORD v17b** (SWOT River Database) — Elizabeth H. Altenau, Tamlin M. Pavelsky, Michael T. Durand, Xiao Yang, Renato P. d. M. Frasson & Liam Bendezu. (2025). SWOT River Database (SWORD) (Version v17b) [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.15299138 · data: https://zenodo.org/records/15299138 · https://www.swordexplorer.com/
- **IRIS-SWORD slope** — Chen, Y., Cohen, S., Baruah, A., Devi, D., Dhital, S., Tian, D., & Munasinghe, D. (2025). Merging Remote Sensing Derived River Slope Datasets with High-Resolution Hydrofabrics for the United States. *Scientific Data*, 12(1), 1657.
- **EGM2008** — Pavlis, N. K., Holmes, S. A., Kenyon, S. C., & Factor, J. K. (2012). The development and evaluation of the Earth Gravitational Model 2008 (EGM2008). *Journal of Geophysical Research: Solid Earth*, 117(B4).
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

## Team

| Name | Institution | GitHub |
|---|---|---|
| Zih-Syun Chen | University of Houston | [@zixunn](https://github.com/zixunn) |
| Sebastian Marshall | Johns Hopkins University | [@rushmarshall](https://github.com/rushmarshall) |
| Pitamber Wagle | Brigham Young University | [@Pitamberwagle](https://github.com/Pitamberwagle) |
| Reza Jamshidi | Northeastern University | [@Reza-Jamshidi](https://github.com/Reza-Jamshidi) |

**Theme leads:** Sagy Cohen and Anupal Baruah, University of Alabama

## Acknowledgements

Built on the OWP HAND-FIM chain and FIMBench, the [SDML lab](https://github.com/sdmlua) `fimeval` / `fimbox` /
`fimserve` tools, the SWORD river database, the SWOT and ICESat-2/IRIS water-surface products, and the National
Water Model.

---
<div align="center">

**CUAHSI Summer Institute 2026** &nbsp;·&nbsp; **Team Slippery Slope**

University of Houston &nbsp;·&nbsp; Johns Hopkins University &nbsp;·&nbsp; Brigham Young University &nbsp;·&nbsp; Northeastern University 

</div>
