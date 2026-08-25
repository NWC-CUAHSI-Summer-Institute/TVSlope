"""The study-area registry, the slope ladder, and the crosswalk gate. Rebuilt locally, not imported.

Nothing here is taken from swot-fim-2026/src/final_config.py. The six areas are re-declared, the benchmark
is chosen by event date (benchmarks.select, which refuses Tier-4 synthetics), and every slope is recomputed
from the SWOT record.

THE SLOPE LADDER (the five panels of the original Ohio figure)
  T0 baseline      the OWP hydrotable as downloaded; no injection
  SWOT-median      median slope over all QC-passed SWOT passes
  SWOT-floodstage  median slope of the TOP-DECILE-WSE passes
  SWOT-maxWSE      slope at the single highest-WSE pass
  gauge S(Q)       the fitted per-reach S(Q) law at the event discharge, CLAMPED to the fitted Q range

Note on SWOT-floodstage and SWOT-maxWSE: they condition on WATER-SURFACE ELEVATION, not on the quantile of
slope. An earlier version of this analysis took the median of the top quartile of SLOPE VALUES and called it
a "high-flow slope". That is the steep tail of the slope distribution, not the slope at high stage. On a
backwater reach the two have OPPOSITE SIGNS, and the mistake inverted the conclusion. Condition on flow.

THE CROSSWALK GATE
A treatment only exists if the SWORD reach actually reaches the hydrotable. SWORD reach -> NWM flowlines
within tol_m -> feature_id -> HydroID rows. If that set is empty, sqrt(S_new/S_old) multiplies nothing, every
treatment equals T0, and the run is a green no-op that answers nothing. The gate asserts it is non-empty.

Author: Sebastian R.O. Marshall
"""
import os
import sys

import numpy as np
import pandas as pd
import geopandas as gpd
import pyogrio

PROJ = "/Users/sebastianmarshall/dev/swot-fim-2026/local_data/proj_mirror"
RUN = "/Users/sebastianmarshall/dev/swot-fim-2026/local_data/run"
SWORD = os.path.join(PROJ, "03_Data", "incoming", "sword_v17b", "gpkg", "na_sword_reaches_v17b.gpkg")
SWOT_TS = os.path.join(PROJ, "06_Results", "results", "swot_slope_timeseries_expanded.csv")
HARLAN_SLOPE = os.path.join(PROJ, "USGS_Gauges_Approach", "GaugeSlope_GRL_Submission", "results",
                            "swot_reach_slope_harlan.csv")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import benchmarks as B

EA = 5070
TOL_M = 1000.0
MIN_PASSES = 8

# The six study areas. fim_huc is where HAND lives; bench_huc is where the benchmark lives (they differ for
# the Mississippi, whose reach sits in 07140105 but whose S1A scene is catalogued under 08010300).
AREAS = [
    dict(reach="75120400053", river="Neches River",      fim_huc="12020003", bench_huc="12020003",
         event=("2017-08-17", "2017-09-01"), dyn="kinematic", gup="08040600", gdn="08041000", gq="08041000"),
    dict(reach="74282100101", river="Illinois River",    fim_huc="07130011", bench_huc="07130011",
         event="2016-01-04", dyn="kinematic", gup="05586100", gdn="05586300", gq="05586100"),
    dict(reach="74270100061", river="Mississippi River", fim_huc="07140105", bench_huc="08010300",
         event="2017-05-04", dyn="backwater", gup="07020850", gdn="07022000", gq="07022000"),
    dict(reach="74267300251", river="Ohio River",        fim_huc="05140101", bench_huc="05140101",
         event="2025-04-12", dyn="backwater", gup="03293551", gdn="03294500", gq="03294500"),
    dict(reach="74282100111", river="Illinois River",    fim_huc="07130011", bench_huc="07130011",
         event="2016-01-04", dyn="kinematic", gup=None, gdn="05585500", gq="05585500"),
    dict(reach="75120400151", river="Neches River",      fim_huc="12020003", bench_huc="12020003",
         event=("2017-08-17", "2017-09-01"), dyn="kinematic", gup=None, gdn="08040600", gq="08040600"),
]


FRESH_TS = os.path.join(PROJ, "06_Results", "results", "fim_rebuild_swot_timeseries.csv")


def swot_ladder(reach):
    """The three SWOT slope treatments for a reach, conditioned on WSE. None when the record is too thin.

    Source order matters, and the first attempt at this got it wrong. The two pre-existing local tables are
    both INCOMPLETE SUBSETS:
      swot_slope_timeseries_expanded.csv  156 curated reaches
      swot_reach_slope_harlan.csv         2,077 reaches, but only those CO-LOCATED WITH GAUGES, and it holds
                                          a median with no WSE, so floodstage/maxWSE are not derivable
    Reading only those two makes four of the six study areas look like they have no SWOT slope. They do. The
    authoritative source is the Hydrocron pull (fim_rebuild/pull_swot.py), which is tried FIRST."""
    out = dict(median=None, floodstage=None, maxwse=None, n=0, source=None)
    for path, tag in ((FRESH_TS, "Hydrocron pull (WSE-conditioned)"),
                      (SWOT_TS, "curated timeseries (WSE-conditioned)")):
        if not os.path.exists(path):
            continue
        d = pd.read_csv(path)
        s = d[d.reach_id.astype(str) == str(reach)].dropna(subset=["slope", "wse"])
        s = s[s.slope > 0]
        if len(s) >= MIN_PASSES:
            out.update(median=float(s.slope.median()),
                       floodstage=float(s.loc[s.wse >= s.wse.quantile(0.90), "slope"].median()),
                       maxwse=float(s.loc[s.wse.idxmax(), "slope"]),
                       n=len(s), source=tag)
            return out
    h = pd.read_csv(HARLAN_SLOPE, dtype={"reach_id": str})
    r = h[h.reach_id == str(reach)]
    if len(r) and float(r.swot_med_slope.iloc[0]) > 0 and int(r.swot_slope_n.iloc[0]) >= MIN_PASSES:
        out.update(median=float(r.swot_med_slope.iloc[0]), n=int(r.swot_slope_n.iloc[0]),
                   source="Harlan median only (no WSE, so no floodstage/maxWSE)")
    return out


def gauge_sq(reach, q_event):
    """The fitted per-reach S(Q) law at the event discharge, CLAMPED to the fit's own support.

    Extrapolating a quadratic beyond its support is the Section 7.6 vertex/zero-crossing pathology. Returns
    (S, note) or (None, why-not)."""
    sys.path.insert(0, os.path.join(PROJ, "USGS_Gauges_Approach", "notebooks"))
    try:
        import sq_core as SQC
    except Exception as e:
        return None, f"sq_core unavailable: {e}"
    if str(reach) not in getattr(SQC, "REACHES", {}):
        return None, "reach has no gauge pair in sq_core.REACHES"
    try:
        p = SQC.sq_pairs(str(reach))
        f = SQC.fit_sq(p.Q_cms.values, p.S.values)
        qlo, qhi = f["Q_range"]
        q = min(float(q_event), float(qhi))
        s = float(f["func"](np.array([q]))[0])
        note = (f"{f['kind']} fit, n={f['n']}, R2={f['all_r2'][f['kind']]:.3f}, support {qlo:,.0f}-{qhi:,.0f}")
        if q_event > qhi:
            note += f"; CLAMPED (event {q_event:,.0f} is {100*(q_event/qhi-1):.0f}% beyond support)"
        if s <= 0:
            return None, note + "; fit returns a non-positive slope, unusable"
        return s, note
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def crosswalk(reach, fim_huc, tol_m=TOL_M):
    """SWORD reach -> NWM feature_ids -> HydroIDs in that HUC's hydrotable. Raises when empty."""
    hucdir = os.path.join(RUN, "output", f"flood_{fim_huc}", fim_huc)
    sw = pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(reach)}")
    sw = sw.set_crs(4326, allow_override=True).to_crs(EA)
    if not len(sw):
        raise SystemExit(f"{reach}: not in SWORD")
    line = sw.union_all()
    st = gpd.read_file(os.path.join(hucdir, "nwm_subset_streams.gpkg")).to_crs(EA)
    idc = "ID" if "ID" in st.columns else st.columns[0]
    near = st[st.geometry.intersects(line.buffer(tol_m))]
    fids = sorted(set(pd.to_numeric(near[idc], errors="coerce").dropna().astype(np.int64)))
    ht = pd.read_csv(os.path.join(hucdir, "hydrotable.csv"), usecols=["HydroID", "feature_id", "SLOPE"])
    hit = ht[ht.feature_id.isin(fids)]
    hids = sorted(hit.HydroID.unique())
    if not hids:
        raise SystemExit(f"{reach}: CROSSWALK GATE FAILED, 0 HydroIDs in HUC {fim_huc}. Every treatment "
                         f"would equal T0 and the run would answer nothing.")
    s = hit.groupby("HydroID").SLOPE.first()
    # RETURN fids, not just their count. The caller needs the actual NWM reach ids: HAND numbers HydroIDs
    # PER BRANCH, so a HydroID alone cannot identify a river, and an injector handed only HydroIDs has to
    # re-derive the feature set from them, which re-imports the collision. feature_id IS globally unique.
    return dict(reach=reach, fim_huc=fim_huc, n_feature_ids=len(fids), n_hydroids=len(hids),
                hydroids=hids, feature_ids=fids,
                slope_median=float(s.median()), reach_km=line.length / 1000.0)


if __name__ == "__main__":
    cat = B.catalog()
    rows = []
    print("=" * 108)
    print("STUDY-AREA REGISTRY")
    print("=" * 108)
    for a in AREAS:
        try:
            bm = B.select(a["bench_huc"], a["event"], cat)
        except Exception as e:
            print(f"\n{a['reach']} {a['river']}: BENCHMARK REFUSED -> {e}")
            continue
        try:
            cw = crosswalk(a["reach"], a["fim_huc"])
        except SystemExit as e:
            print(f"\n{a['reach']} {a['river']}: {e}")
            continue
        sw = swot_ladder(a["reach"])
        print(f"\n{a['reach']}  {a['river']:<20} [{a['dyn']}]")
        print(f"   benchmark : {bm['tier']} {bm['res_m']} m   {bm['site']}")
        print(f"   crosswalk : {cw['n_hydroids']} HydroIDs from {cw['n_feature_ids']} feature_ids"
              f"   (reach {cw['reach_km']:.1f} km, hydrotable SLOPE median {cw['slope_median']*1e6:,.0f} mm/km)")
        if sw["median"] is None:
            print(f"   SWOT      : NO USABLE SLOPE (n<{MIN_PASSES} or non-positive). "
                  f"Only T0 can be run for this reach.")
        else:
            print(f"   SWOT      : n={sw['n']}  median={sw['median']*1e6:,.0f} mm/km"
                  + (f"  floodstage={sw['floodstage']*1e6:,.0f}  maxWSE={sw['maxwse']*1e6:,.0f} mm/km"
                     if sw["floodstage"] is not None else "  (median only)")
                  + f"   [{sw['source']}]")
        rows.append(dict(reach=a["reach"], river=a["river"], dyn=a["dyn"], fim_huc=a["fim_huc"],
                         bench_huc=a["bench_huc"], tier=bm["tier"], res_m=bm["res_m"], scene=bm["site"],
                         n_hydroids=cw["n_hydroids"], hydro_slope_mmkm=cw["slope_median"] * 1e6,
                         swot_n=sw["n"],
                         swot_median=sw["median"], swot_floodstage=sw["floodstage"], swot_maxwse=sw["maxwse"],
                         swot_source=sw["source"]))
    df = pd.DataFrame(rows)
    out = os.path.join(PROJ, "06_Results", "results", "fim_rebuild_registry.csv")
    df.to_csv(out, index=False)
    print(f"\nwrote {out}  ({len(df)} areas)")
