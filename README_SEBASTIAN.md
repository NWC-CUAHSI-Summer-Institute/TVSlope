# `sebastian_branch`: time-varying gauge slope S(Q), Sebastian's working notebook

This branch **adds** a parallel line of work alongside `main`. Nothing on `main` is modified:
`code/TV_Slope_FIM.ipynb` and `code/tvslope_src/` are untouched, and every file here is new.

The notebook shares only a small part of its cell source with `code/TV_Slope_FIM.ipynb`. Treat the two
as two separate readings of the same research question rather than as one file and its edit.

## What this branch adds

| Path | What it is |
|---|---|
| `notebooks/work_0607.ipynb` | The notebook, 59 cells, with all outputs kept so it reads without being run |
| `notebooks/sq_core.py` | The S(Q) chain rebuilt against the public USGS NWIS API, so Step 7 runs anywhere |
| `src/` | The analysis modules the notebook imports, plus the study-area registry and benchmark gate |
| `stage_local_root.py` | The staging script, kept mainly for the data-tree manifest in its docstring |

## The contribution

Beyond the static-satellite baseline (IRIS-SWORD, Chen 2025) and the time-varying SWOT slopes, the
notebook introduces a **time-varying gauge slope**: two paired stations give a water-surface slope that
varies with discharge, `S(Q)`, which is fitted per reach and injected into the Manning synthetic rating
curve. Because the uncalibrated SRC is Manning, injecting a slope rescales discharge by
`sqrt(S_new / S_0)` at fixed stage. Seventeen SWOT-observed reaches span the hydraulic-regime axis,
separating reaches where slope rises with flow (kinematic) from reaches where it falls (backwater).

## What runs, and where

Three tiers, stated plainly so nobody loses an afternoon to the third:

1. **Reading the notebook needs nothing.** Every figure and table is embedded in the committed outputs.
2. **Step 7 (the S(Q) sections) runs anywhere.** `sq_core.py` pulls from the public USGS NWIS API and
   caches each response, so these cells execute on a clean machine with only a network connection.
   `src/timevarying_slope.py` imports `per_reach3`, which reads author-local CSVs at import time, so
   Step 7 deliberately does not depend on it. `sq_core.py` mirrors the same chain, and the notebook
   asserts that the mirror reproduces the production fits before using it.
3. **Everything else needs the staged data tree.** Cell 2 resolves `ROOT` to a `slipperyslope/` tree in
   this order: `$SLIPPERYSLOPE_ROOT`, then `/Users/zixun/2026SI/slipperyslope`, then
   `<repo>/slipperyslope`. The docstring of `stage_local_root.py` lists exactly what that tree must
   contain and which line of which module reads each item. The FIM scoring cell additionally needs the
   flood-extent run outputs (tens of GB), which no branch can carry.

Everything staged is real data already fetched from the operational sources: FIMBench benchmarks
(sdmlua fimeval), flood extents from NOAA-OWP inundation-mapping on the OWP HAND 4.9.9.0 cache, and the
Harlan et al. (2026) SWOT-gauge pairing (USGS ScienceBase, 10.5066/P1FE9W9E).

## Environment

The repository  already covers what  needs,  included, so
Step 7 runs in the  environment as it stands. One cell of the notebook draws a CONUS context map
with , which  does not list. Install it alongside, or skip that one cell.

## Known limits of this branch

- `src/areas.py`, `src/benchmarks.py` and `stage_local_root.py` hard-code paths under the author's
  `local_data/` mirror. They import cleanly, and their functions need those paths to exist. Point them
  at a local copy of the tree before calling them.
- `notebooks/work_0607.ipynb` is about 74 MB, because the high-resolution figures and two animations are
  embedded. GitHub will not render a file that size in the browser, so pull the branch and open it
  locally.
- The NWIS response cache is not committed. Step 7 refetches on first run and caches from there.

## Two things worth a second look

Both are recorded in the source comments, and both changed a conclusion:

- **Condition on flow, not on the slope quantile.** `swot_floodstage` and `swot_maxwse` condition on
  water-surface elevation. An earlier version took the median of the top quartile of slope *values* and
  called it a high-flow slope. On a backwater reach those two have opposite signs, and the substitution
  inverted the result.
- **The benchmark is selected by event date, never by glob order.** `src/benchmarks.py` refuses Tier-4
  synthetic design floods outright, so a real flood can never be scored against a 500-year design event
  simply because the filesystem returned it first.

Author: Sebastian R.O. Marshall
