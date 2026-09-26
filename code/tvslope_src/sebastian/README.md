# Source modules

Reusable Python behind the notebooks. Notebooks import from here; they do not redefine logic inline.

| Module | Responsibility |
|---|---|
| `slope_injection` | Rescale Manning discharge by sqrt(S_new / S_old) and rebuild the rating curve |
| `rating_curve` | Synthetic rating curve construction and stage-discharge inversion |
| `data_access` | SWOT, IRIS, USGS, and SWORD readers with the quality-control filters applied |

Modules land here as the workflow stabilizes during the sprint.
