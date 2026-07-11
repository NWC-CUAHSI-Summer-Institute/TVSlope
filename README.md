<h1 align="center">TVSlope</h1>
<p align="center"><b>Time-varying river slope in HAND-FIM synthetic rating curves</b></p>
<p align="center">
  <img src="https://img.shields.io/badge/python-3.10-3776AB?logo=python&logoColor=white" alt="python">
  <img src="https://img.shields.io/badge/Jupyter-notebooks-F37626?logo=jupyter&logoColor=white" alt="jupyter">
  <img src="https://img.shields.io/badge/HAND--FIM-flood%20inundation-1f77b4" alt="hand-fim">
  <img src="https://img.shields.io/badge/data-SWOT%20%C2%B7%20IRIS%20%C2%B7%20NWM%20%C2%B7%20FIMBench-2ca02c" alt="data">
  <img src="https://img.shields.io/badge/reproducible-self--contained%20notebooks-success" alt="reproducible">
</p>

<p align="center"><i>Does replacing the river slope in operational HAND flood-inundation mapping with a
satellite-derived or a time-varying gauge-derived product measurably change flood-map skill, and where (by
hydraulic regime) does it matter?</i></p>

<p align="center"><img src="output_final/figures/workflow_architecture.png" width="88%" alt="workflow"></p>

---

## Overview

Operational OWP **HAND** flood-inundation mapping (FIM) turns National Water Model (NWM) discharge into flood
extent through a Manning **synthetic rating curve (SRC)**. Because the uncalibrated SRC is Manning
(*Q* &propto; &radic;*S*), the river **slope** *S* is a first-order control on the rating curve. This repository
evaluates, end to end and against the **FIMBench** benchmark, whether a better slope makes a better flood map:

- a **static-satellite** baseline (IRIS-SWORD; Chen et al., 2025) and three **SWOT**-derived slopes, and
- a new **time-varying gauge slope** *S(Q)*: from two paired gauges we form the water-surface slope
  *S*(*t*) = (WSE<sub>up</sub> &minus; WSE<sub>dn</sub>)/*L*, pair it with the on-reach discharge *Q*(*t*), fit a
  non-linear *S(Q)*, and inject it into every hydro-table row by iterating *Q* = *Q*<sub>0</sub>&radic;(*S(Q)*/*S*<sub>0</sub>).

**Headline finding.** Across six SWOT-observed reaches, the slope source (and even its flow dependence) is a
**second-order** control on flood extent; the **hydraulic regime** — whether the reach is free-flowing
(kinematic) or backwater — is **first-order**. An order-of-magnitude slope range collapses to a few-hundredths
range in CSI, because the &radic;*S* Manning dependence compresses slope into conveyance and terrain ultimately
sets the extent.

## What's inside

| Notebook | What it does |
|---|---|
| [`code/study_area.ipynb`](code/study_area.ipynb) | Selects the SWOT-observed study reaches: the SWORD river network gated on FIMBench benchmark coverage and on same-river up/on/down USGS gauge triplets required by the paired-gauge slope method. |
| [`code/timevary_slope.ipynb`](code/timevary_slope.ipynb) | Develops the time-varying gauge slope *S(Q)* method over the full reach selection: paired-gauge slope vs discharge, iterative Manning injection, subprocess HAND-FIM, and River-Mask CSI/F1. |
| [`code/work6_3DHRS.ipynb`](code/work6_3DHRS.ipynb) | The focused six-reach study and manuscript figures: static-satellite vs gauge time-varying *S(Q)* slope, scored against FIMBench on the River-Mask domain, with the Results & Discussion. |

Each notebook is **fully self-contained** — the entire slope / FIM / scoring engine is inlined in its setup cell
(no local module imports) — resolves paths relative to the repository root, and writes every figure at **300 dpi**
as both PNG and SVG.

## Installation

```bash
git clone https://github.com/zixunn/TVSlope.git
cd TVSlope
conda env create -f environment.yml   # numpy, pandas, geopandas, rasterio, scipy, matplotlib, contextily, dataretrieval, ...
conda activate slope
```

The analysis runs on the packages above. Regenerating FIM from scratch additionally needs the `fimbox` HAND-FIM
package and is gated behind `REGEN_FIM` / `TVS_REGEN` (off by default — the notebooks reuse the cached extents).

## Quick start

```bash
# render the flagship six-reach study end to end (uses the cached FIM extents)
jupyter nbconvert --to notebook --execute --inplace code/work6_3DHRS.ipynb
# or open interactively
jupyter lab code/work6_3DHRS.ipynb
```

Paths are portable: the notebooks find the repo root via the `.slope_root` marker (override with the `SLOPE_ROOT`
environment variable), so they run whether launched from the repo root or a subfolder.

## Method &amp; workflow

```
reach selection            slope treatments              HAND-FIM + scoring
──────────────────         ─────────────────────         ────────────────────────────
SWORD ∩ FIMBench       →   hydrofabric (reference)   →   inject slope into the SRC
same-river gauge           IRIS-SWORD (baseline)         (Manning rescale / iterative S(Q))
triplets (study_area)      SWOT median/floodstage/           │
                           maxWSE                        NWM forcing: retrospective in-window,
                           gauge time-varying S(Q)           operational forecast post-2023
                              (this work)                    │
                                                         score vs FIMBench on the RIVER MASK
                                                         (reach NWM catchments; largest CC)
                                                             │
                                                         CSI · F1 · POD · FAR  →  regime analysis
```

Two design choices make the comparison defensible: **(1)** every event is forced by one NWM family (retrospective,
or the operational short-range forecast for post-2023 floods — never a substituted gauge); **(2)** every metric is
computed on the **river mask** (the union of the reach's NWM catchments, benchmark cleaned to its largest connected
component), which removes the large off-channel false-negative term that a whole-benchmark score would impose.

## Data

Following good practice, the repository commits **only the small derived tables that cannot be queried from a
public service**; everything else is fetched or generated by the workflow (see [`DATA.md`](DATA.md) for the full
manifest, sizes, and sources).

| Committed here (`data/`) | Fetched / generated by the workflow (not committed) |
|---|---|
| `FIMHF_IRIS_new.csv`, `FIMHF_IRIS_v1.0.csv` — IRIS-SWORD satellite slopes (Chen et al., 2025) | **USGS** stage/discharge — auto-fetched via `dataretrieval` (cached under `data/`) |
| `slope_treatments.csv` — SWOT-derived slope products per reach | **SWORD** reach network — download from the SWORD data portal |
| `study_area_gauges.csv` — the same-river gauge triplets from `study_area.ipynb` | **FIMBench** benchmarks — download from the OWP FIM benchmark dataset |
|  | **NWM** discharge (retrospective / operational forecast) and the **staged HAND** cache — generated by the FIMbox pipeline |

`work6_3DHRS.ipynb` reads a small cached FIM extent set; `study_area.ipynb` and `timevary_slope.ipynb` need the
full reference layers. `DATA.md` documents exactly what each notebook reads and how to obtain it (including
optional Git LFS packaging for a clone-and-run work6 bundle).

## Examples

<table>
<tr>
<td width="50%"><img src="output_final/figures/aoi_maps_2x3.png" alt="study reaches"><br><sub><b>Six study reaches</b> — SWOT reach, FIMBench flood extent, and the river-mask evaluation domain.</sub></td>
<td width="50%"><img src="output_final/figures/sq_relationship.png" alt="S(Q)"><br><sub><b>Slope&ndash;discharge <i>S(Q)</i></b> — slope steepens with flow on the kinematic Illinois, flattens on the backwater Ohio.</sub></td>
</tr>
<tr>
<td width="50%"><img src="output_final/figures/src_all_reaches.png" alt="rating curves"><br><sub><b>Synthetic rating curves</b> per reach and treatment; the dashed line marks the discharge that drove each event's FIM.</sub></td>
<td width="50%"><img src="output_final/figures/csi_f1_per_reach.png" alt="skill"><br><sub><b>Flood-map skill (CSI, F1)</b> by slope treatment, scored on the river-mask domain.</sub></td>
</tr>
</table>

All figures and tables are regenerated into [`output_final/`](output_final/) by running `work6_3DHRS.ipynb`.

## Reproducibility

- Self-contained notebooks (no local imports); portable paths (`.slope_root` / `SLOPE_ROOT`).
- Deterministic figures at 300 dpi (PNG + SVG); the Results & Discussion pull every number live from the tables.
- FIM (re)generation is optional and reproducible via `REGEN_FIM=True` (work6) / `TVS_REGEN=1` (timevary).

## Citation

If you use this code or the derived slope products, please cite this repository and the IRIS-SWORD source
(Chen et al., 2025). A `CITATION.cff` and a license file can be added to finalize distribution.

## Acknowledgements

Built on the OWP HAND-FIM chain and FIMBench, the SWORD river database, the SWOT and ICESat-2/IRIS
water-surface products, and the National Water Model.
