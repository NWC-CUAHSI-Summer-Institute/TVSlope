# tvslope_src — study code for TV_Slope_FIM

Python code behind `TV_Slope_FIM.ipynb` (time-varying river-slope HAND flood-inundation study).

- `engine/` — the analysis: study configuration, gauge discharge/stage/WSE series, time-varying
  slope `S(Q)`, reach↔NWM matching, FIM-vs-benchmark scoring, the AOI map figures, and FIM output lookup.
- `fimbox_ext/` — the FIMbox-wrapping drivers that build the HAND and generate the FIM flood extents.

## Source tools

This study is built on the following open-source tools.

| Tool | Role in this study | Source |
| --- | --- | --- |
| NOAA-OWP/inundation-mapping | The operational HAND-FIM method (relative elevation model, synthetic rating curves, flood-extent mosaicking) that FIMbox implements | https://github.com/NOAA-OWP/inundation-mapping |
| FIMbox | HAND-FIM engine, called from source on every run: stages the NWM hydrofabric + 3DEP DEM, builds HAND and the synthetic rating curves, and generates the FIM extent | https://github.com/sdmlua/fimbox |
| FIMserv | HAND-FIM staging/serving; provides the conda environment the notebook runs in | https://github.com/sdmlua/FIMserv |
| FIMeval | FIM-vs-benchmark CSI / contingency scoring; the same categorical metrics are computed on a river-mask domain in `engine/fim_eval.py` | https://github.com/sdmlua/fimeval |
| FIMbench | The multi-source benchmark flood maps (optical / SAR / high-water-mark) used as ground truth for scoring | https://github.com/sdmlua/fimbench |
| RiverJoin | River-line matching across hydrofabrics (SWORD ↔ NWM); reach ↔ feature_id resolution is done in `engine/fim_reach.py` | https://github.com/sdmlua/riverjoin_py |

## How each tool is used

- **FIMbox** — `fimbox_ext/fimbox_uncalibrated.py` runs one AOI × slope-product end to end with calibration
  off (`getAllInputData` → `BranchDerivation` + `calculate_allbranches` → `getNWMretrospective` → `generateFIM`);
  `fimbox_ext/build_branch_zero.py` builds and prunes FIMbox's branch 0 to a tributary gap-filler;
  `fimbox_ext/regen_subdiv_fim.py` and `regen_operational_fim.py` orchestrate per-treatment slope injection and
  run the FIM for the retrospective and NWM-operational-forecast events.
- **NOAA-OWP/inundation-mapping** — the HAND-FIM methodology FIMbox implements; no code is vendored, but the
  method (HAND relative elevation + Manning synthetic rating curve → flood extent) is the FIM engine of this study.
- **FIMserv** — supplies the staging/serving dependency stack; the notebook runs in its conda environment.
- **FIMeval** — benchmark access plus CSI / POD / FAR / F1 contingency scoring; `engine/fim_eval.py` computes the
  same metrics restricted to the reach's river-mask domain.
- **FIMbench** — the benchmark flood-map dataset each FIM is scored against.
- **RiverJoin** — matching SWOT/SWORD reaches to NWM feature_ids; `engine/fim_reach.py` performs this
  reach-to-feature_id join.

FIMbox itself is installed in its own environment at `/Users/zixun/2026SI/FIMBox_github/fimbox` and is called
from source; it is not vendored into this folder. Files in `fimbox_ext/` carry a header noting the FIMbox source.

## Attribution

Study code by Zih-Syun Chen `<emily30823@gmail.com>`. Upstream tools belong to their authors (NOAA-OWP; the
Surface Dynamics Modeling Lab, University of Alabama).
