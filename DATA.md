# Data layout & how to publish this on GitHub

The three notebooks are **self-contained code** (no local module imports) and resolve every path relative to
the repository root (`_repo_root()` in the setup cell: `$SLOPE_ROOT`, else the nearest parent holding a
`.slope_root` marker or a `data/` folder). So the code is trivially shareable — the only real question is the
**data**, which totals ~59 GB and cannot live in a git repo as-is.

The strategy below splits the data into three tiers: **(A) commit to git**, **(B) commit via Git LFS**, and
**(C) host externally** (Zenodo / Google Drive / S3) with a download script.

---

## 1. What each notebook reads (input manifest)

| Notebook | Reads (inputs) | Writes (outputs) |
|---|---|---|
| `work6_3DHRS.ipynb` | `data/slope_treatments.csv`; `data/SWORD_v17b_gpkg/…` (6 reaches, queried by id); `data/FIMBench/<6 events>/*_BM.tif` + `*_AOI.gpkg`; `data/fimbox_out/HUC{05140101,07130011,07140105,10170203,10230003}/` → `fim-outputs/*.tif`, `discharge-inputs/*.csv`, `watershed-data/*_subset_streams.gpkg`, `*catchments_proj_subset.gpkg`, `branches/*/hydroTable_*.csv.orig`; `data/paired_reach_SWOT_gage/…` (coords only); `data/twin_gauge/`, `data/discharge/` (gauge cache); `data/us_states.gpkg` | `output_final/` (figures PNG+SVG, tables, dossier) |
| `gauge_study.ipynb` | `data/SWORD_v17b_gpkg/…` (CONUS, 3.7 GB); `data/usgs_gages.gpkg`; `data/paired_reach_SWOT_gage/…`; `data/us_states.gpkg`; USGS NWIS (auto via `dataretrieval`) | `output_gauge/` |
| `study_area.ipynb` | `data/SWORD_v17b_gpkg/…` (CONUS, 3.7 GB); `data/usgs_gages.gpkg`; `data/paired_reach_SWOT_gage/…`; `data/benchmark_domain_t123hwm.gpkg`; `data/GDW/` (dams); FIMBench (auto-downloaded via `fimeval`) | `output_study_area/` |
| `timevary_slope.ipynb` | `data/SWORD_v17b_gpkg/…`; `data/FIMBench/…`; `data/FIMHF_IRIS_new.csv`; `data/discharge/`, `data/twin_gauge/`; `data/fimbox_out/HUC*/` (18 HUCs, cache) | `output_study_area/timevary/` |
| `swot_geoid_slope.ipynb` | `data/swot_hydrocron_study_reaches.csv`; `data/swot_study_reach_nodes.csv`; `data/swot_study_reaches_sword.csv` (all committed — no SWORD download needed); PROJ geoid grids (EGM2008 / EGM96 / NAVD88, fetched from the PROJ CDN on first use and cached) | `output_final/tables/swot_datum_verification.csv`, `output_final/tables/geoid_slope_sensitivity.csv`, `output_final/figures/geoid_datum_slope.{png,svg}` |

**Sizes that matter** (`du -sh`):

| Path | Size | Tier |
|---|---:|---|
| `data/fimbox_out` (all staged HAND, 18+ HUCs) | 34 GB | C (external) |
| `data/SWORD_v17b_gpkg` (CONUS reach network) | 3.7 GB | C (external) — or a 6-reach subset in git |
| `data/FIMBench` (all benchmark tiles) | 4.0 GB | C (external) |
| `data/IRIS_*`, `data/GDW`, `data/fimserv`, `FIMHF_IRIS_v1.0.gpkg` | ~17 GB | C (external) |
| **work6 minimal cache** (6 HUCs `fim-outputs`) | **111 MB** | B (LFS) |
| work6 6 HUCs `watershed-data` small files (streams+catchments gpkg + `hydroTable*.orig`) | ~0.3–0.5 GB | B (LFS) |
| work6 6 FIMBench `*_BM.tif` (Ohio 0.2 m 521 MB + Illinois 0.4 m 465 MB dominate) | ~1.0 GB | B (LFS) — **clip first, see §4** |
| `data/slope_treatments.csv`, `data/study_area_gauges.csv` | < 1 MB | A (git) |
| `data/swot_hydrocron_study_reaches.csv`, `data/swot_study_reach_nodes.csv`, `data/swot_study_reaches_sword.csv` | 1.8 MB | A (git) |

---

## 2. Recommended repository layout

```
<your-repo>/
  .slope_root                 # marker so the notebooks find the root from any subfolder
  .gitignore  .gitattributes  # provided here (LFS for *.tif/*.tiff/*.nc only)
  environment.yml             # conda env
  README.md  DATA.md
  code/                       # the 3 notebooks (or rename to notebooks/)
    work6_3DHRS.ipynb
    timevary_slope.ipynb
    study_area.ipynb
  data/                       # inputs (see tiers) — small tables in git, cache via LFS, big layers external
    slope_treatments.csv
    study_area_gauges.csv
    SWORD_v17b_gpkg/          # (external, or a 6-reach subset)
    FIMBench/                 # (external, or clipped 6-event subset via LFS)
    fimbox_out/HUC*/          # (external, or work6's small subset via LFS)
    ...
  output_final/               # work6 outputs (regenerated; commit if you want them viewable on GitHub)
```

Notebook paths need **no editing** — they already use `ROOT/"data"/…`. If you move the notebooks into a
`notebooks/` folder, the resolver still works (it walks up to `.slope_root`).

---

## 3. Publishing — the three tiers

### Tier A — commit directly (small, non-queryable) — this is what this repo ships
`environment.yml`, `README.md`, `DATA.md`, `.slope_root`, `.gitignore`, `.gitattributes`, the 3 notebooks,
`output_final/`, and the derived tables that cannot be fetched from a public service:
`data/FIMHF_IRIS_new.csv`, `data/FIMHF_IRIS_v1.0.csv` (IRIS-SWORD slopes),
`data/slope_treatments.csv` (SWOT slope products), `data/study_area_gauges.csv` (gauge triplets),
and the three SWOT/SWORD extracts that make the vertical-datum notebook reproducible without the
3.7 GB SWORD download: `data/swot_hydrocron_study_reaches.csv` (1.1 MB, the Hydrocron pull for the
study reaches), `data/swot_study_reach_nodes.csv` (680 KB, the SWORD node chain — coordinates and
`dist_out` — for those reaches), `data/swot_study_reaches_sword.csv` (12 KB, reach centroids).
Everything else is fetched (USGS via `dataretrieval`; SWORD / FIMBench downloads) or generated (NWM / staged HAND).

### Tier B — commit via Git LFS (the curated work6 cache, so `git clone` runs work6)
`data/fimbox_out/HUC{5 study HUCs}/{fim-outputs, discharge-inputs}` + the small `watershed-data` vector/rating
files, the 6 `FIMBench` benchmarks (clipped, §4), and a **6-reach SWORD subset** (§4). ~200–400 MB after
clipping; comfortably within a GitHub repo + LFS. (GitHub free LFS = 1 GB storage / 1 GB month bandwidth; bump
the quota if you keep full-resolution benchmarks.)

### Tier C — host externally + download script (everything heavy)
Full `SWORD_v17b_gpkg`, full `FIMBench`, full `fimbox_out`, `IRIS_*`, `GDW`, `fimserv`. Upload a single
`slope_data.zip` to **Zenodo** (gets a DOI, ideal for a paper) or Google Drive / S3, and ship a
`scripts/download_data.sh` that fetches + unpacks it into `data/`. `study_area.ipynb` and `timevary_slope.ipynb`
need this tier (their inputs are tens of GB); `work6_3DHRS.ipynb` does not if you ship Tier B.

---

## 4. Make `work6` clone-and-run (shrink Tier B)

Two size drivers: the CONUS SWORD (3.7 GB) and two full-res benchmarks (Ohio 0.2 m 521 MB, Illinois 0.4 m
465 MB). Both shrink to a few MB without changing any result, because the notebook only ever reads the 6 reaches
and only the benchmark pixels inside each reach's evaluation domain.

```bash
# (a) 6-reach SWORD subset (3.7 GB -> a few hundred KB); notebook queries by reach_id so this is a drop-in
ogr2ogr -f GPKG data/SWORD_v17b_gpkg/na_sword_reaches_v17b_subset.gpkg \
        data/SWORD_v17b_gpkg/na_sword_reaches_v17b.gpkg na_sword_reaches_v17b \
        -where "reach_id IN (74295200111,74295100321,74270100061,74267300251,74282100111,74282100101)"
#     then point the notebook SWORD constant at the subset (or just commit the subset under the same name).

# (b) clip each big benchmark to a ~15 km box around its reach (521 MB -> ~10 MB), keeps CSI identical
#     because scoring is windowed to the river mask. Use gdalwarp -te <xmin ymin xmax ymax> in the tile CRS.
```

A small helper that generates both is worth adding as `scripts/make_work6_bundle.py`; ask if you want it.

---

## 5. Commands — push to GitHub

This repo already ships **Tier A** (notebooks + config + derived tables + `output_final/`). To publish it:

```bash
cd TVSlope
git remote add origin git@github.com:zixunn/TVSlope.git   # repo already created on github.com
git push -u origin main
```

To additionally publish the **Tier B** curated work6 cache so `git clone` runs work6 (needs Git LFS; the
`.gitattributes` here already tracks `*.tif *.gpkg *.parquet`):

```bash
git lfs install
git add data/fimbox_out/HUC*/fim-outputs data/fimbox_out/HUC*/discharge-inputs \
        'data/fimbox_out/HUC*/watershed-data/*_subset_streams.gpkg' \
        'data/fimbox_out/HUC*/watershed-data/*catchments_proj_subset.gpkg' \
        'data/fimbox_out/HUC*/watershed-data/branches/*/hydroTable_*.csv.orig' \
        data/SWORD_v17b_gpkg/na_sword_reaches_v17b_subset.gpkg \
        data/FIMBench          # (clipped events only, §4)
git commit -m "Add curated work6 FIM cache (LFS)"
git push
```

Verify LFS took the binaries: `git lfs ls-files` should list the `.tif`/`.gpkg` files.

---

## 6. Reproduce after clone

```bash
git clone <repo> && cd <repo>
git lfs pull                              # fetch the LFS binaries
conda env create -f environment.yml && conda activate slope
# work6 runs on the committed Tier-B cache:
jupyter nbconvert --to notebook --execute --inplace code/work6_3DHRS.ipynb
# study_area / timevary additionally need the Tier-C archive:
bash scripts/download_data.sh             # (fetches SWORD/FIMBench/fimbox_out into data/)
```
