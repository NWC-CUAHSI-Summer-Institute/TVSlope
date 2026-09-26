"""Benchmark scene selection: by event DATE and tier, never by glob order.  # sebastian update

Why this exists. Resolving a benchmark with a glob and taking the first hit --

    bm = sorted(glob(".../FIMBench/{huc}/**/*BM*.tif"))[0]

-- lets the filesystem decide what a flood is scored against. For HUC 12020003 the FIMBench catalog
offers two scenes: a 10 m high-water-mark map of Hurricane Harvey, and `Tier_4 BLE_500`, a 500-year
SYNTHETIC DESIGN FLOOD produced by a hydraulic model. A glob can therefore score Harvey against a
design flood, and nothing downstream would notice.

The rule enforced here:

    ELIGIBLE   Tier_1, Tier_2, Tier_3, HWM    (all OBSERVATIONS of a real flood)
    REFUSED    Tier_4                         (BLE synthetic design floods -- raises, never silently taken)

Among eligible scenes, pick the finest resolution whose date matches the event.

Ported from Sebastian Marshall's `benchmarks.py`. Two changes were needed to make it run outside the
author's machine: the catalog is built from data committed to this repository plus whatever
`get_data.py` has downloaded, instead of a CSV in a local mirror; and `SystemExit` became
`RuntimeError`, which does not kill a Jupyter kernel.

On this study's staged tree the gate is latent -- only one scene is staged per HUC, so no published
number depends on it. It is a rail, not a correction.
"""

from __future__ import annotations

import glob
import os
import re

import pandas as pd

from final_config import DATA

__all__ = ["ELIGIBLE", "REFUSED", "SyntheticBenchmarkRefused", "scene_dates", "catalog", "select", "paths"]

ELIGIBLE = ("Tier_1", "Tier_2", "Tier_3", "HWM")   # observed floods
REFUSED = ("Tier_4",)                              # synthetic design floods (BLE)
TIER_RANK = {"Tier_1": 0, "Tier_2": 1, "Tier_3": 2, "HWM": 3}

FIMBENCH = DATA / "FIMBench"                        # populated by code/get_data.py
_GAUGES = DATA / "study_area_gauges.csv"            # committed; carries fimbench_id / _tier / _huc8


class SyntheticBenchmarkRefused(Exception):
    """Raised when the only benchmark on offer for the event is a synthetic design flood."""


def scene_dates(site: str) -> list[str]:
    """Every yyyymmdd embedded in a FIMBench scene name, as ISO dates.

    Names look like AI_20250412_854320W381510N, HWM_20170817_20170901_940714W300838N,
    S1A_20170504T23553_891934W365313N. The trailing token is a coordinate, not a date, so only
    8-digit runs that parse as a plausible date are kept.
    """
    out = []
    for tok in re.findall(r"\d{8}", str(site)):
        y, m, d = int(tok[:4]), int(tok[4:6]), int(tok[6:])
        if 1990 <= y <= 2030 and 1 <= m <= 12 and 1 <= d <= 31:
            out.append(f"{y:04d}-{m:02d}-{d:02d}")
    return out


def _res_m(name: str) -> float:
    """Resolution in metres from a FIMBench filename, e.g. AI_0_2m_2025... -> 0.2, HWM_10_0m -> 10.0."""
    m = re.search(r"_(\d+)_(\d+)m_", str(name))
    if m:
        return float(f"{m.group(1)}.{m.group(2)}")
    m = re.search(r"_(\d+)m_", str(name))
    return float(m.group(1)) if m else float("nan")


def _from_committed() -> list[dict]:
    """Catalog rows from the committed study-area table (tier is recorded there per reach)."""
    if not _GAUGES.exists():
        return []
    g = pd.read_csv(_GAUGES, dtype=str)
    rows = []
    for _, r in g.dropna(subset=["fimbench_id"]).iterrows():
        parts = str(r.fimbench_id).split("/")
        if len(parts) < 2:
            continue
        tier, site = parts[0], parts[1]
        leaf = parts[-1]
        for h in str(r.get("fimbench_huc8", "") or "").split(";"):
            h = h.strip()
            if h:
                rows.append(dict(huc8=h.zfill(8), tier=tier, site=site, res_m=_res_m(leaf),
                                 dates=scene_dates(site), source="committed"))
    return rows


def _from_download() -> list[dict]:
    """Catalog rows scanned from whatever get_data.py has actually downloaded."""
    if not FIMBENCH.is_dir():
        return []
    rows = []
    for hdir in sorted(FIMBENCH.iterdir()):
        if not hdir.is_dir():
            continue
        for scene in sorted(hdir.iterdir()):
            if not scene.is_dir():
                continue
            bm = sorted(scene.glob("*_BM.tif"))
            leaf = bm[0].name if bm else scene.name
            # the tier is not in the download path; infer the observation class from the scene prefix
            tier = "HWM" if scene.name.startswith("HWM") else "Tier_1"
            for h in hdir.name.split(";"):                 # a scene folder can span several HUC8s
                h = h.strip()
                if h:
                    rows.append(dict(huc8=h.zfill(8), tier=tier, site=scene.name, res_m=_res_m(leaf),
                                     dates=scene_dates(scene.name), source="download"))
    return rows


def _from_declared() -> list[dict]:
    """Catalog rows for the scenes the study configuration names explicitly.

    `final_config.AREAS` pins an `event` scene for some reaches. Those must be in the catalog or the
    gate would silently substitute a different scene for them -- which is the very failure mode it
    exists to prevent, only in the other direction.
    """
    try:
        from final_config import AREAS
    except Exception:
        return []
    rows = []
    for a in AREAS:
        site = a.get("event")
        if not site:
            continue
        tier = "HWM" if str(site).startswith("HWM") else "Tier_1"
        h = str(a.get("bench_huc", a.get("huc", ""))).strip()
        if h:
            rows.append(dict(huc8=h.zfill(8), tier=tier, site=site, res_m=float("nan"),
                             dates=scene_dates(site), source="declared"))
    return rows


def catalog() -> pd.DataFrame:
    """Every (scene, HUC8) pair this machine knows about, from committed data and downloads.

    The committed rows carry the authoritative tier; download rows fill in scenes that were fetched
    but are not referenced by the study table. Committed rows win on a collision.
    """
    rows = _from_declared() + _from_committed() + _from_download()
    if not rows:
        return pd.DataFrame(columns=["huc8", "tier", "site", "res_m", "dates", "source"])
    c = pd.DataFrame(rows)
    c["_pref"] = c.source.map({"declared": 2, "committed": 1, "download": 0}).fillna(0)
    c = c.sort_values("_pref", ascending=False).drop_duplicates(["huc8", "site"]).drop(columns="_pref")
    return c.reset_index(drop=True)


def select(bench_huc, event_date, cat: pd.DataFrame | None = None, prefer: str | None = None) -> dict:
    """The one benchmark scene to score against, chosen by date then by tier and resolution.

    `event_date` is an ISO date or an (start, end) window; a scene matches when ANY of its embedded
    dates falls inside it. Raises SyntheticBenchmarkRefused when the only date-matched option is Tier_4.

    `prefer` is a scene the caller has already pinned (`final_config.AREAS[...]["event"]`). When it is
    eligible and its date matches, it WINS -- the gate validates the pinned choice rather than
    overriding it, so adding this rail does not silently move any existing result. It still refuses a
    pinned Tier_4.
    """
    cat = catalog() if cat is None else cat
    lo, hi = (event_date, event_date) if isinstance(event_date, str) else event_date
    sub = cat[cat.huc8 == str(bench_huc).zfill(8)]
    if not len(sub):
        raise RuntimeError(f"no benchmark scene known for HUC {bench_huc}. Run code/get_data.py.")

    matched = sub[sub.dates.apply(lambda ds: any(lo <= d <= hi for d in ds))]
    if not len(matched):
        avail = sorted({d for ds in sub.dates for d in ds})
        raise RuntimeError(f"HUC {bench_huc}: no benchmark scene dated in {lo}..{hi}. Available: {avail}")

    ok = matched[matched.tier.isin(ELIGIBLE)]
    if not len(ok):
        bad = sorted(set(matched.tier))
        raise SyntheticBenchmarkRefused(
            f"HUC {bench_huc}: the only benchmark dated in {lo}..{hi} is {bad}. Tier_4 is a synthetic "
            f"design flood (BLE), not an observation of this event. Refusing to score against it.")

    if prefer:
        pinned = ok[ok.site == prefer]
        if len(pinned):
            b = pinned.iloc[0]
            return dict(bench_huc=str(bench_huc).zfill(8), site=b.site, tier=b.tier,
                        res_m=float(b.res_m), dates=b.dates, dropped=[], pinned=True)
        if (matched.site == prefer).any():        # pinned but not eligible -> that is a refusal
            t = matched[matched.site == prefer].tier.iloc[0]
            raise SyntheticBenchmarkRefused(
                f"HUC {bench_huc}: the pinned scene {prefer} is {t}, which is not an observation "
                f"of this event. Refusing to score against it.")

    ok = ok.assign(rank=ok.tier.map(TIER_RANK)).sort_values(["rank", "res_m"])
    best = ok.iloc[0]
    return dict(bench_huc=str(bench_huc).zfill(8), site=best.site, tier=best.tier,
                res_m=float(best.res_m), dates=best.dates,
                dropped=sorted(set(matched.tier) - {best.tier}), pinned=False)


def paths(bench_huc, site):
    """The downloaded BM raster and AOI polygon for a scene, under data/FIMBench/."""
    pats = [str(FIMBENCH / f"*{str(bench_huc).zfill(8)}*" / "**"), str(FIMBENCH / "**")]
    bm, aoi = [], []
    for p in pats:
        bm += glob.glob(os.path.join(p, "*_BM.tif"), recursive=True)
        aoi += glob.glob(os.path.join(p, "*_AOI.gpkg"), recursive=True)
        if bm:
            break
    key = str(site).replace("_", "")

    def match(p):
        return site in p or key in os.path.basename(p).replace("_", "")

    bm = [p for p in bm if match(p)] or bm
    aoi = [p for p in aoi if match(p)] or aoi
    return (sorted(bm)[0] if bm else None), (sorted(aoi)[0] if aoi else None)


if __name__ == "__main__":
    c = catalog()
    print(f"catalog: {len(c)} (scene, HUC8) pairs over {c.huc8.nunique()} HUC8s")
    print(c.tier.value_counts().to_string())
    from final_config import AREAS
    print(f"\n{'reach':<14}{'benchHUC':<11}{'tier':<9}{'res':>6}  scene / verdict")
    for a in AREAS:
        bh = a.get("bench_huc", a["huc"])
        try:
            s = select(bh, a["bench_date"], c, prefer=a.get("event"))
            bm, _ = paths(bh, s["site"])
            tag = "pinned" if s.get("pinned") else "by rank"
            print(f"{a['reach']:<14}{bh:<11}{s['tier']:<9}{s['res_m']:>6.1f}  {s['site']}"
                  f"  [{tag}; {'on disk' if bm else 'not downloaded'}]")
        except SyntheticBenchmarkRefused as e:
            print(f"{a['reach']:<14}{bh:<11}{'REFUSED':<9}{'-':>6}  {e}")
        except RuntimeError as e:
            print(f"{a['reach']:<14}{bh:<11}{'-':<9}{'-':>6}  {e}")
