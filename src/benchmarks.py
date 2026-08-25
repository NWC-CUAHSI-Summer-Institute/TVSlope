"""Benchmark registry for the FIM rebuild. Selection is by EVENT DATE, never by glob order.

Why this file exists. `swot-fim-2026/src/final_config.py:88-91` resolves a benchmark like this:

    bm = clip or sorted(glob(".../FIMBench/{huc}/**/*BM*.tif")) or sorted(glob(".../FIMBench/{huc}/**/*.tif"))

It takes bm[0]. Whatever the filesystem hands back first wins. For HUC 12020003 the catalog offers exactly
two benchmarks: a 10 m HWM map of Harvey, and `Tier_4 BLE_500`, a 500-YEAR SYNTHETIC DESIGN FLOOD produced
by a hydraulic model. A glob can therefore score Hurricane Harvey against a design flood, and nothing in the
code would notice. That is the most dangerous line in the work config.

The rule enforced here, per the author's decision:
  ELIGIBLE   Tier_1, Tier_2, Tier_3, HWM   (all OBSERVATIONS of a real flood)
  REFUSED    Tier_4                        (BLE synthetic design floods; raises, never silently selected)
Among eligible scenes, pick the FINEST resolution whose date matches the event.

Author: Sebastian R.O. Marshall
"""
import os
import re
import glob

import pandas as pd

PROJ = "/Users/sebastianmarshall/dev/swot-fim-2026/local_data/proj_mirror"
CATALOG = os.path.join(PROJ, "06_Results", "results", "fimbench_catalog.csv")
RUN = "/Users/sebastianmarshall/dev/swot-fim-2026/local_data/run"

ELIGIBLE = ("Tier_1", "Tier_2", "Tier_3", "HWM")   # observed floods
REFUSED = ("Tier_4",)                              # synthetic design floods (BLE)
TIER_RANK = {"Tier_1": 0, "Tier_2": 1, "Tier_3": 2, "HWM": 3}


class SyntheticBenchmarkRefused(Exception):
    """Raised when the only benchmark on offer is a synthetic design flood."""


def scene_dates(site):
    """Every yyyymmdd embedded in a FIMBench scene name, as ISO dates.

    Names look like AI_20250412_854320W381510N, HWM_20170817_20170901_940714W300838N,
    S1A_20170504T23553_891934W365313N. The trailing token is a coordinate, not a date, so only
    8-digit runs that parse as a plausible date are kept."""
    out = []
    for tok in re.findall(r"\d{8}", site):
        y, m, d = int(tok[:4]), int(tok[4:6]), int(tok[6:])
        if 1990 <= y <= 2030 and 1 <= m <= 12 and 1 <= d <= 31:
            out.append(f"{y:04d}-{m:02d}-{d:02d}")
    return out


def catalog():
    c = pd.read_csv(CATALOG, dtype=str)
    c["res_m"] = pd.to_numeric(c.res_m, errors="coerce")
    rows = []
    for _, r in c.iterrows():
        for h in str(r.huc8).split(";"):                      # scenes can span several HUC8s
            rows.append(dict(huc8=h.strip(), tier=r.tier, site=r.site, res_m=r.res_m,
                             state=r.state, dates=scene_dates(r.site)))
    return pd.DataFrame(rows)


def select(bench_huc, event_date, cat=None):
    """The one benchmark scene to score against, chosen by date then by resolution.

    `event_date` may be a single ISO date or an (start, end) window. A scene matches when ANY of its
    embedded dates falls in the window. Raises SyntheticBenchmarkRefused when the only date-matched
    option is Tier_4."""
    cat = catalog() if cat is None else cat
    lo, hi = (event_date, event_date) if isinstance(event_date, str) else event_date
    sub = cat[cat.huc8 == str(bench_huc).zfill(8)]
    if not len(sub):
        raise SystemExit(f"no benchmark scene in the catalog for HUC {bench_huc}")

    matched = sub[sub.dates.apply(lambda ds: any(lo <= d <= hi for d in ds))]
    if not len(matched):
        raise SystemExit(f"HUC {bench_huc}: no benchmark scene dated in {lo}..{hi}. "
                         f"Available: {sorted({d for ds in sub.dates for d in ds})}")

    ok = matched[matched.tier.isin(ELIGIBLE)]
    if not len(ok):
        bad = sorted(set(matched.tier))
        raise SyntheticBenchmarkRefused(
            f"HUC {bench_huc}: the only benchmark dated in {lo}..{hi} is {bad}. Tier_4 is a synthetic "
            f"design flood (BLE), not an observation of this event. Refusing to score against it.")

    ok = ok.assign(rank=ok.tier.map(TIER_RANK)).sort_values(["rank", "res_m"])
    best = ok.iloc[0]
    return dict(bench_huc=str(bench_huc).zfill(8), site=best.site, tier=best.tier,
                res_m=float(best.res_m), dates=best.dates,
                dropped=sorted(set(matched.tier) - {best.tier}))


def paths(bench_huc, site):
    """The downloaded BM raster and AOI polygon for a scene, under ~/swot_fim_runs/bench_<huc>/."""
    root = os.path.join(RUN, f"bench_{str(bench_huc).zfill(8)}")
    bm = [p for p in glob.glob(os.path.join(root, "**", "*_BM.tif"), recursive=True)]
    aoi = [p for p in glob.glob(os.path.join(root, "**", "*_AOI.gpkg"), recursive=True)]
    # a scene folder is named for the site, so keep only the files belonging to THIS scene
    key = site.replace("_", "")
    def match(p):
        return site in p or key in os.path.basename(p).replace("_", "")
    bm = [p for p in bm if match(p)] or bm
    aoi = [p for p in aoi if match(p)] or aoi
    return (bm[0] if bm else None), (aoi[0] if aoi else None)


if __name__ == "__main__":
    cat = catalog()
    print(f"catalog: {len(cat)} (scene, HUC8) pairs over {cat.huc8.nunique()} HUC8s\n")
    # the six original study areas, as declared in swot-fim-2026/src/final_config.py:28-51
    AREAS = [
        ("75120400053", "Neches",      "12020003", "12020003", ("2017-08-17", "2017-09-01")),
        ("74282100101", "Illinois",    "07130011", "07130011", "2016-01-04"),
        ("74270100061", "Mississippi", "07140105", "08010300", "2017-05-04"),
        ("74267300251", "Ohio",        "05140101", "05140101", "2025-04-12"),
        ("74282100111", "Illinois",    "07130011", "07130011", "2016-01-04"),
        ("75120400151", "Neches",      "12020003", "12020003", ("2017-08-17", "2017-09-01")),
    ]
    print(f"{'reach':<14}{'river':<13}{'benchHUC':<10}{'tier':<8}{'res':>6}  scene / verdict")
    for reach, river, fh, bh, ev in AREAS:
        try:
            s = select(bh, ev, cat)
            bm, aoi = paths(bh, s["site"])
            have = "on disk" if bm else "NOT DOWNLOADED"
            drop = f"  (dropped: {s['dropped']})" if s["dropped"] else ""
            print(f"{reach:<14}{river:<13}{bh:<10}{s['tier']:<8}{s['res_m']:>6.1f}  {s['site']}  [{have}]{drop}")
        except SyntheticBenchmarkRefused as e:
            print(f"{reach:<14}{river:<13}{bh:<10}{'REFUSED':<8}{'-':>6}  {e}")
