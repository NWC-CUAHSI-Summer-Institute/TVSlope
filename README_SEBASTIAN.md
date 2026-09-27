# Integrated from `sebastian_branch`

Sebastian Marshall's `sebastian_branch` was a parallel reading of the same research question, carrying
its own engine (`src/`), its own notebook (`work_0607.ipynb`) and a portable `S(Q)` mirror
(`sq_core.py`). The parts of it that the main line lacked have been integrated into
`code/tvslope_src/engine/`, and the parallel tree has been removed so the repository has one engine
rather than two. Integrated code carries a `# sebastian update` marker.

Author of the original analysis and of the four contributions below: **Sebastian R.O. Marshall**
(Johns Hopkins University, [@rushmarshall](https://github.com/rushmarshall)).

## What was integrated, and why it mattered

| Now at | What it fixes |
|---|---|
| `engine/fim_eval.py` → `permanent_water()`, wired into `score_rm()` | FIMBench benchmarks are **observed-water** maps, so they contain the river sitting in its own channel. Those pixels are not a flood. In a 12 km box on the Ohio they are 12,774 of 25,906 benchmark-wet pixels — **49.3%** of everything the benchmark calls wet. A HAND-FIM that leaves the channel dry put every one of them in FN. The operational `fimeval` scorer gives permanent water its own class and excludes it; the main line did not. |
| `engine/reach_mask.py` | The **causal footprint** of a slope treatment, and the invariant that follows: if the flood map changes *outside* the catchments the injection touched, the injection touched something it should not have. That is not a metric, it is a correctness test — and it caught a real bug, where HydroIDs (which HAND numbers *per branch*) were used as the injection key and 52% of the rescaled rows were the wrong river. |
| `engine/benchmarks.py` | Benchmark selection by **event date and tier**, never by glob order. For HUC 12020003 the catalog offers both a high-water-mark map of Hurricane Harvey and `Tier_4 BLE_500`, a 500-year synthetic design flood. A glob could score Harvey against a design flood and nothing would notice. Tier_4 is now refused, loudly. |
| `engine/fim_reach.py` → the slope-treatment chain, and `per_reach3.swot_clean()` | The **provenance of `data/slope_treatments.csv`**. That table was committed data with no code in the main line that could rebuild it. |

Two changes were needed to make the ported code run outside the author's machine, plus one correction:

- **No hard-coded local paths.** The originals resolved a data root through
  `/Users/sebastianmarshall/dev/...` and `/Users/zixun/2026SI/slipperyslope`. The ports resolve
  everything through `final_config._repo_root()` and the committed `data/` tree.
- **`SystemExit` → `RuntimeError`**, so a refusal does not kill a Jupyter kernel.
- **The gauge slope is now datum-harmonised.** `gauge_slope()` goes through the engine's
  `per_reach3.twin_series`, which puts both gauges on one vertical datum before differencing them. The
  original did not, and 7 of 78 twin-gauge pairs in this study straddle NAVD88 and NGVD29. See the
  README's "Vertical datum" section.

## What was not carried over

- `sq_core.py` — a portable `S(Q)` chain rebuilt against the public USGS NWIS API. Its portability is
  now met by `engine/per_reach3`, which reads committed extracts and caches NWIS responses itself. Its
  other value was as an *independent* cross-check that asserted it reproduced the production fits; that
  cross-check is lost with it.
- `areas.py`, `find_reaches3.py` — a separate study-area registry and 3-gauge reach finder, superseded
  by `final_config.AREAS` and notebooks 01–02.
- `stage_local_root.py` — a staging script for the author's local mirror.
- `fim_reach.build_hand_once` / `generate_fim_for_reach` / `generate_treatment_fim` — a monolithic FIM
  generation path. The main line generates FIM through `code/tvslope_src/fimbox_ext/` instead.
- `notebooks/work_0607.ipynb` — the notebook itself, which depended on a staged tree outside this
  repository. Its conclusions over 17 reaches are not reproduced here.

The full pre-integration state is recoverable: it is the `sebastian_branch` ref on
`NWC-CUAHSI-Summer-Institute/TVSlope`, and it remains in this repository's history.
