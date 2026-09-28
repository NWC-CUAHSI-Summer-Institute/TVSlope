"""sq_core - self-contained S(Q) engine for the Step 7 slope-discharge section.

WHY THIS FILE EXISTS
--------------------
`sebastian/timevarying_slope.py` (TV) is the production S(Q) engine, but it imports `per_reach3`,
which reads two of Zixun's local CSVs *at module import time* under
ROOT = /Users/zixun/2026SI/slipperyslope. On any other machine `import timevarying_slope`
raises before a single function runs, so the Step 7 cells cannot call TV at all.

This module re-implements the exact same chain against the public USGS NWIS API, caching
every response to CSV under `tvslope_src/sebastian/sq_cache/`. It reproduces TV's published fits to
three significant figures (see `verify_against_notebook()`), so it is a faithful mirror,
not a second method.

  TV chain                              sq_core mirror
  ------------------------------------  ---------------------------------------
  per_reach3.stage_series               dv(g, "00065")        NWIS dv, ft -> m
  per_reach3.datum                      site_info(g)["alt_m"] site service alt_va
  per_reach3.wse_series                 wse = alt_m + gh
  per_reach3.twin_series                twin_series()         S = (wse_up - wse_dn)/L
  final_config._gauge_span_km           span_m()              haversine, r = 6371.0 km
  timevarying_slope.sq_pairs            sq_pairs()            S>0 & Q>0, MAD k=5.0
  timevarying_slope.fit_sq              fit_sq()              quadratic vs powerlaw by R2
  timevarying_slope._solve_Q            solve_Q()             Q = Q0 sqrt(S(Q)/S0)

Every quality-control constant below carries its provenance in PROVENANCE, and every
citation in REFERENCES was verified against the Crossref API before being written here.

Author: Sebastian R.O. Marshall
"""
from __future__ import annotations

import time
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

# --------------------------------------------------------------------------------------
# Units. Identical to per_reach3.FT / per_reach3.CFS.
# --------------------------------------------------------------------------------------
FT = 0.3048                  # international foot -> m
CFS = 0.028316846592         # cubic foot per second -> m3/s
R_EARTH_KM = 6371.0          # matches final_config._gauge_span_km
MM_PER_KM = 1e6              # slope in m/m -> mm/km

CACHE = Path(__file__).resolve().parent / "sq_cache"
CACHE.mkdir(exist_ok=True)

# --------------------------------------------------------------------------------------
# The two gauge-paired reaches. Metadata copied verbatim from final_config.areas_df().
# `gq` is the station supplying on-reach discharge Q(t).
# --------------------------------------------------------------------------------------
REACHES = {
    "74282100101": dict(
        river="Illinois River", dyn_class="kinematic",
        gup="05586100", gdn="05586300", gq="05586100",
        fim_huc8="07130011", bench_date="2016-01-04", fim_driver="nwm",
        q_flood_cms=3200.0,
    ),
    "74267300251": dict(
        river="Ohio River", dyn_class="backwater",
        gup="03293551", gdn="03294500", gq="03294500",
        fim_huc8="05140101", bench_date="2025-04-12", fim_driver="gauge",
        q_flood_cms=15631.0,
    ),
}

# ---------------------------------------------------------------------------------------
# Cross-site validation reaches, carried over from
#   USGS_Gauges_Approach/notebooks/NB_USGS_Gauges_Slope.ipynb  (cell 8, dict THREE)
#
# Those reaches are three-gauge reaches; that notebook picks the pair with the LONGEST
# overlapping record, which is what `gup`/`gdn` below record. `span_m` is the along-channel
# distance (the difference of the two gauges' `dist_out` from the reach outlet), NOT a
# great-circle distance, so it is given explicitly rather than recomputed by haversine.
#
# Only the two reaches whose own pair gauges report discharge are carried here. The other
# three (Cumberland x2, White River 74266400361) have no discharge at either pair gauge and
# depend on a borrowed or drainage-area-transferred series, which would add a confound this
# section is not trying to test.
#
# `status` is that notebook's CLEAN / impacted label. It is NOT taken on faith: `structure`
# below records an independent OpenStreetMap Overpass query for dams, weirs and lock gates in
# a window straddling each pair (run 2026-07-09).
# ---------------------------------------------------------------------------------------
# `q_source` records where the on-reach discharge actually comes from, because this is the gate
# that eliminates most candidates:
#   "pair gauge"   one of the two stage stations also reports discharge
#   "third gauge"  a THIRD station on the same SWORD reach reports it (still an on-reach measurement)
#   "transferred"  discharge is scaled from a donor gauge by a drainage-area ratio. NOT a measurement
#                  of this reach, so Step 7 declines to fit an S(Q) curve to it.
# `span_m` is the along-channel distance from USGS_Gauges_Approach/results/gauge_slope_master.csv
# (`dist_m`), which NB_USGS_Gauges_Slope measures along the SWORD centreline, not as a great circle.
XREACHES = {
    "73260900321": dict(
        river="Chattahoochee R, GA", dyn_class=None, status="CLEAN",
        gup="02335990", gdn="02336000", gq="02336000", q_source="pair gauge",
        span_m=1093.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Overpass returned no dam, weir or lock gate between the gauges."),
    "74266400321": dict(
        river="White R, IN", dyn_class=None, status="impacted",
        gup="03353000", gdn="03353611", gq="03353611", q_source="pair gauge",
        span_m=4191.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Downstream gauge 03353611 sits at Stout Generating Station; a weir is mapped "
             "within the pair. Its daily stage record is absent, so NB_USGS_Gauges_Slope used "
             "instantaneous stage resampled to a daily median. That series is cached here."),
    # ---- carried in 2026-07-09 after auditing every candidate pair, not only the four plotted --
    "NEUSE": dict(
        river="Neuse R, NC", dyn_class=None, status="pair",
        gup="02089000", gdn="02089192", gq="02089192", q_source="pair gauge",
        span_m=18214.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Self-found co-located pair. The six OSM structures inside its bounding box are all "
             "off-channel lake dams, 889 m or further from the NHDPlus centreline. See "
             "STRUCTURES_ON_RIVER: none sits on the river."),
    "CAPEFEAR": dict(
        river="Cape Fear R, NC", dyn_class=None, status="pair",
        gup="02104000", gdn="02105500", gq="02105500", q_source="pair gauge",
        span_m=24000.0, dv_start="2010-01-01", q_flood_cms=None,
        note="The downstream station is named CAPE FEAR R AT WILM O HUSKE LOCK NR TARHEEL, so the "
             "lock and dam is at the gauge. Its slope nevertheless RISES with discharge."),
    "PEEDEE": dict(
        river="Great Pee Dee R, SC", dyn_class=None, status="pair",
        gup="02131000", gdn="02131010", gq="02131010", q_source="pair gauge",
        span_m=5241.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Self-found co-located pair, no mapped structure on the river centreline."),
    # ---- candidates that FAIL a Step 7 gate. Kept so the ledger can compute the failure, not assert it.
    "CUMB_071": dict(
        river="Cumberland R, TN (Bordeaux)", dyn_class=None, status="impacted",
        gup="03431514", gdn="03431712", gq="03431500", q_source="third gauge",
        span_m=5994.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Neither stage station reports discharge; 03431500 (Nashville) does, on the same "
             "reach. Fails the backwater gate: the water surface runs uphill on 16.5% of days."),
    "CUMB_081": dict(
        river="Cumberland R, TN (Inglewood)", dyn_class=None, status="CLEAN",
        gup="03430320", gdn="03431091", gq="03431500", q_source="transferred",
        donor="03431500", da_ratio=0.997,
        span_m=9573.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Discharge is drainage-area-scaled from 03431500. Also fails the backwater gate "
             "(10.7% uphill days)."),
    "WHITE_361": dict(
        river="White R, IN (Broad Ripple)", dyn_class=None, status="impacted",
        gup="03351005", gdn="03351071", gq=None, q_source="transferred",
        donor="03351000", da_ratio=1.016,
        span_m=4814.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Donor 03351000 is not carried into this repo, so no discharge series exists here. "
             "It fails the on-reach-discharge gate regardless. Three weirs sit on its centreline, "
             "one of them Broad Ripple Dam, and the downstream station is named WHITE RIVER BELOW "
             "DAM AT BROAD RIPPLE."),
    "GREENBRIER": dict(
        river="Greenbrier R, WV", dyn_class=None, status="pair",
        gup="03182890", gdn="03182970", gq=None, q_source="transferred",
        donor="03183500", da_ratio=0.841,
        span_m=7493.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Discharge drainage-area-scaled from 03183500, which is not cached here."),
    "MERAMEC": dict(
        river="Meramec R, MO", dyn_class=None, status="pair",
        gup="07019130", gdn="07019210", gq=None, q_source="transferred",
        donor="07019000", da_ratio=1.024,
        span_m=6033.0, dv_start="2010-01-01", q_flood_cms=None,
        note="Discharge drainage-area-scaled from 07019000, which is not cached here."),
}

ALL_REACHES = {**REACHES, **XREACHES}

# The four reaches Figures 7.1 and 7.2 draw. Kept explicit so a later reach cannot silently join them.
PLOTTED = ["74282100101", "73260900321", "74266400321", "74267300251"]

# Landmarks drawn on the locator map. Coordinates are NOT estimated: each carries a source.
LANDMARKS = {
    "74267300251": [
        dict(name="McAlpine Locks and Dam", lat=38.2782686, lon=-85.7911117,
             source="OpenStreetMap way/817753482 (ODbL), queried 2026-07-09"),
    ],
    "74266400321": [
        dict(name="Harding Street Power Plant Dam", lat=39.7100503, lon=-86.2016029,
             source="OpenStreetMap way/80765265, waterway=weir (ODbL), queried 2026-07-09"),
    ],
    # Chattahoochee 73260900321: an Overpass query over the window straddling the pair
    # (33.8560,-84.4600,33.8720,-84.4480) returned zero dam / weir / lock_gate features.
    # Absence of a mapped structure is recorded as absence of an entry, never as a marker.
}

# --------------------------------------------------------------------------------------
# Structures that sit ON the river, not merely inside a bounding box around the pair.
#
# A bounding box around an 18 km gauge pair catches every farm pond and lake dam in the box.
# The Neuse's six Overpass hits are all off-channel lake dams. The discriminator is distance to
# the NHDPlus flowline, fetched from the USGS NLDI upstream-main navigation of the DOWNSTREAM
# gauge (the downstream-main navigation from Illinois 05586100 returns zero features).
#
# TOL_M is not load-bearing. Across all 12 candidates the furthest KEPT structure is 118 m and
# the nearest DROPPED one is 209 m, a 91 m gap, so any tolerance in (118, 209) gives this table.
STRUCT_TOL_M = 150.0
STRUCTURES_ON_RIVER = {
    "74266400321": [dict(name="Harding Street Power Plant Dam", osm="way/80765265", kind="weir", dist_m=54)],
    "74267300251": [dict(name="McAlpine Dam Lower Gates", osm="way/817753487", kind="dam", dist_m=88)],
    "CAPEFEAR":    [dict(name="William O Huske Lock and Dam Number 3", osm="node/357810713", kind="dam", dist_m=23)],
    "WHITE_361":   [dict(name="(unnamed)", osm="node/944741754", kind="weir", dist_m=34),
                    dict(name="Broad Ripple Dam", osm="way/50893290", kind="weir", dist_m=35),
                    dict(name="(unnamed)", osm="way/172058646", kind="weir", dist_m=118)],
    # Zero on-river structures, each verified against the NHDPlus centreline rather than assumed:
    #   74282100101 Illinois, 73260900321 Chattahoochee, CUMB_071, CUMB_081 (Cheek Dam, 422 m off),
    #   NEUSE (6 box hits, nearest 889 m off), PEEDEE, GREENBRIER, MERAMEC.
}

# --------------------------------------------------------------------------------------
# Quality-control constants and where each one comes from.
# `basis` is one of: "physical", "standard", "instrument", "inherited".
# "inherited" means the value was carried over from the production code with no published
# justification. Section 7.7 runs a sensitivity sweep over every inherited constant,
# because a reviewer will ask (see Kallestrup-style guidance and the Methods guide, sec. 7).
# --------------------------------------------------------------------------------------
PROVENANCE = {
    "SIGMA_H_M": dict(
        value=0.015, basis="instrument",
        note="USGS stage accuracy spec: +/- 0.01 ft (0.003 m) or 0.2% of effective stage, "
             "whichever is greater. The Illinois and Ohio stage ranges are of order 5-15 m, "
             "so 0.2% gives 0.010-0.030 m; 0.015 m is the mid-range value used here.",
        cite=["sauer2010"]),
    "MAD_K": dict(
        value=5.0, basis="inherited",
        note="Outlier rejection threshold on log(S) and log(Q), in scaled-MAD units. Carried "
             "over from timevarying_slope.sq_pairs. No published basis. Swept in section 7.7.",
        cite=[]),
    "MAD_SCALE": dict(
        value=1.4826, basis="standard",
        note="Consistency factor making the median absolute deviation an unbiased estimator "
             "of the standard deviation under a normal distribution.",
        cite=[]),
    "MIN_N": dict(
        value=8, basis="inherited",
        note="Minimum surviving (Q,S) pairs before a fit is attempted. Carried over from "
             "timevarying_slope.sq_pairs. Both reaches here have n > 3900, so it never binds.",
        cite=[]),
    "SLOPE_CLIP_Q": dict(
        value=(0.005, 0.995), basis="inherited",
        note="Quantile clip applied to the raw S(t) series when n > 20, from "
             "per_reach3.twin_series. Removes the extreme 1% of slopes. Swept in section 7.7.",
        cite=[]),
    "POSITIVITY_GATE": dict(
        value="S > 0 and Q > 0", basis="physical",
        note="A downstream-falling water surface and a positive discharge. Negative S is "
             "either sensor noise, a datum error, or genuine flow reversal; none of the three "
             "belongs in a Manning slope-discharge fit.",
        cite=["iso9123"]),
    "MANNING_RESCALE": dict(
        value="Q = Q0 * sqrt(S(Q)/S0)", basis="physical",
        note="Manning's equation at fixed stage gives Q proportional to S^(1/2), so swapping "
             "the slope from S0 to S(Q) rescales the synthetic rating curve discharge by the "
             "square root of their ratio. Solved by damped fixed-point iteration in solve_Q.",
        cite=["nobre2011", "durand2023"]),
    "SIGNAL_TO_DATUM_MIN": dict(
        value=3.0, basis="inherited",
        note="A pair is usable only if its median head drop exceeds 3x the summed published datum "
             "accuracies of the two gauges. Verbatim from NB_USGS_Gauges_Slope cell 25: "
             "single_slope_valid = (signal_to_datum > 3) & (frac_neg < 0.10), with "
             "signal_to_datum = |median(wse_up - wse_dn)| / (alt_acy_up + alt_acy_dn). "
             "The factor 3 has no published basis and is swept alongside the other constants.",
        cite=["sauer2010"]),
    "FRAC_NEG_MAX": dict(
        value=0.10, basis="inherited",
        note="Maximum share of days on which the water surface runs uphill (S <= 0) before a "
             "single downstream slope stops being a meaningful description of the reach. Also "
             "from NB_USGS_Gauges_Slope cell 25. This is the gate that eliminates both Cumberland "
             "pairs, at 16.5% and 10.7% uphill days.",
        cite=["iso9123"]),
    "R2_FLOOR": dict(
        value=0.25, basis="inherited",
        note="Below this the fitted S(Q) explains too little variance for the sign of dS/dQ to "
             "carry information, whatever its bootstrap interval says. Introduced here, not in the "
             "production code, because the Neuse fit (R2 = 0.10) otherwise reports a confident "
             "falling slope. It is a reporting threshold, not a rejection gate.",
        cite=[]),
    "STRUCT_TOL_M": dict(
        value=150.0, basis="inherited",
        note="Distance from the NHDPlus centreline within which an OpenStreetMap dam, weir or "
             "lock gate counts as sitting ON the river. Not load-bearing: the furthest kept "
             "structure is 118 m and the nearest dropped one 209 m, so any value in that gap "
             "reproduces STRUCTURES_ON_RIVER exactly.",
        cite=["usgs_nldi"]),
}

# --------------------------------------------------------------------------------------
# References. EVERY DOI below was resolved through https://api.crossref.org/works/{DOI}
# and its authors, journal, year, volume and pages checked against the string here.
# Crossref's /works/ endpoint is case-sensitive; the lowercase forms are what resolve.
# --------------------------------------------------------------------------------------
REFERENCES = {
    "scherer2023": dict(
        doi="10.1038/s41597-023-02215-x", verified=True,
        text="Scherer, D., Schwatke, C., Dettmering, D., et al. (2023). ICESat-2 river surface "
             "slope (IRIS): A global reach-scale water surface slope dataset. Scientific Data, 10."),
    "scherer2022": dict(
        doi="10.1029/2022wr032842", verified=True,
        text="Scherer, D., Schwatke, C., Dettmering, D., et al. (2022). ICESat-2 based river "
             "surface slope and its impact on water level time series from satellite altimetry. "
             "Water Resources Research, 58."),
    "altenau2021": dict(
        doi="10.1029/2021wr030054", verified=True,
        text="Altenau, E. H., Pavelsky, T. M., Durand, M. T., et al. (2021). The Surface Water "
             "and Ocean Topography (SWOT) Mission River Database (SWORD). Water Resources "
             "Research, 57."),
    "nobre2011": dict(
        doi="10.1016/j.jhydrol.2011.03.051", verified=True,
        text="Nobre, A. D., Cuartas, L. A., Hodnett, M., et al. (2011). Height Above the Nearest "
             "Drainage, a hydrologically relevant new terrain model. Journal of Hydrology, 404, 13-29."),
    "mansanarez2016": dict(
        doi="10.1002/2016WR018916", verified=True,
        text="Mansanarez, V., Le Coz, J., Renard, B., et al. (2016). Bayesian analysis of "
             "stage-fall-discharge rating curves and their uncertainties. Water Resources "
             "Research, 52, 7424-7443."),
    "petersen2009": dict(
        doi="10.1002/hyp.7417", verified=True,
        text="Petersen-Overleir, A., & Reitan, T. (2009). Bayesian analysis of stage-fall-discharge "
             "models for gauging stations affected by variable backwater. Hydrological Processes, "
             "23, 3057-3074."),
    "fread1975": dict(
        doi="10.1111/j.1752-1688.1975.tb00674.x", verified=True,
        text="Fread, D. L. (1975). Computation of stage-discharge relationships affected by "
             "unsteady flow. JAWRA, 11, 213-228."),
    "hidayat2011": dict(
        doi="10.5194/hess-15-2717-2011", verified=True,
        text="Hidayat, H., Vermeulen, B., Sassi, M. G., et al. (2011). Discharge estimation in a "
             "backwater affected meandering river. Hydrology and Earth System Sciences, 15, 2717-2728.",
        note="The S(Q) methods guide attributes this DOI to 'Besnard & Goutal (2011)'. Crossref "
             "returns Hidayat et al. The guide's attribution is wrong; this entry is the record."),
    "liu2023": dict(
        doi="10.1029/2023GL106394", verified=True,
        text="Liu, Y., Bauer-Gottwein, P., Frias, M. C., et al. (2023). Stage-slope-discharge "
             "relationships upstream of river confluences revealed by satellite altimetry. "
             "Geophysical Research Letters, 50."),
    "bauergottwein2024": dict(
        doi="10.3390/rs16214010", verified=True,
        text="Bauer-Gottwein, P., Christoffersen, J., Musaeus, C., et al. (2024). Hydraulics of "
             "time-variable water surface slope in rivers observed by satellite altimetry. "
             "Remote Sensing, 16, 4010."),
    "gleason2020": dict(
        doi="10.3390/rs12071107", verified=True,
        text="Gleason, C. J., & Durand, M. T. (2020). Remote sensing of river discharge: A review "
             "and a framing for the discipline. Remote Sensing, 12, 1107.",
        note="The S(Q) methods guide cites this as Water Resources Research. Crossref returns "
             "Remote Sensing 12(7):1107. The guide's journal is wrong."),
    "durand2023": dict(
        doi="10.1029/2021wr031614", verified=True,
        text="Durand, M., Gleason, C. J., Pavelsky, T. M., et al. (2023). A framework for "
             "estimating global river discharge from the Surface Water and Ocean Topography "
             "satellite mission. Water Resources Research, 59."),
    "frasson2023": dict(
        doi="10.1175/jhm-d-22-0078.1", verified=True,
        text="Frasson, R. P. de M., Turmon, M., Durand, M., et al. (2023). Estimating the relative "
             "impact of measurement, parameter, and flow law errors on discharge from the Surface "
             "Water and Ocean Topography mission. Journal of Hydrometeorology, 24, 425-443."),
    "moramarco2008": dict(
        doi="10.1061/(ASCE)1084-0699(2008)13:11(1078)", verified=True,
        text="Moramarco, T., Pandolfo, C., & Singh, V. P. (2008). Accuracy of kinematic wave and "
             "diffusion wave approximations for flood routing. I: Steady analysis. Journal of "
             "Hydrologic Engineering, 13, 1078-1088."),
    "enzminger2024": dict(
        doi="10.1038/s41597-024-03916-7", verified=True,
        text="Enzminger, T. L., Minear, J. T., & Livneh, B. (2024). HyG: A hydraulic geometry "
             "dataset derived from historical stream gage measurements across the conterminous "
             "United States. Scientific Data, 11."),
    "mcmahon2019": dict(
        doi="10.1080/02626667.2019.1577555", verified=True,
        text="McMahon, T. A., & Peel, M. C. (2019). Uncertainty in stage-discharge rating curves: "
             "application to Australian Hydrologic Reference Stations data. Hydrological Sciences "
             "Journal, 64, 255-275.",
        note="The S(Q) methods guide attributes this DOI to 'Coles et al. (2019)'. Crossref "
             "returns McMahon & Peel. The guide's attribution is wrong."),
    "dottori2009": dict(
        doi="10.5194/hess-13-847-2009", verified=True,
        text="Dottori, F., Martina, M. L. V., & Todini, E. (2009). A dynamic rating curve approach "
             "to indirect discharge measurement. Hydrology and Earth System Sciences, 13, 847-863.",
        note="The guide cites the HESSD discussion preprint (6, 859-896). This is the published record."),
    "sauer2010": dict(
        doi="10.3133/tm3a7", verified=True,
        text="Sauer, V. B., & Turnipseed, D. P. (2010). Stage measurement at gaging stations. "
             "USGS Techniques and Methods 3-A7."),
    "turnipseed2010": dict(
        doi="10.3133/tm3a8", verified=True,
        text="Turnipseed, D. P., & Sauer, V. B. (2010). Discharge measurements at gaging stations. "
             "USGS Techniques and Methods 3-A8."),
    # Sources with no DOI. Kept separate and explicitly marked so nothing is invented.
    "iso9123": dict(
        doi=None, verified=False,
        text="ISO 9123:2017. Hydrometry, stage-fall-discharge relationships. International "
             "Organization for Standardization.",
        note="Standards body document, no DOI. Not retrievable through Crossref."),
    "usgs_nwis": dict(
        doi=None, verified=False,
        text="U.S. Geological Survey. National Water Information System (NWIS) daily values and "
             "site service. https://waterservices.usgs.gov/",
        note="Data source, accessed 2026-07-09."),
    "hydroschool": dict(
        doi=None, verified=False,
        text="HydroSchool. Rating curves, part 2. https://hydroschool.org/rating2/",
        note="Teaching resource supplied by the author. Contains no equations and cites no "
             "primary literature, so it anchors intuition only, never a numerical claim."),
    "osm_mcalpine": dict(
        doi=None, verified=False,
        text="OpenStreetMap contributors. McAlpine Locks and Dam, way/817753482. ODbL.",
        note="Queried 2026-07-09 for the locator-map marker."),
    "usgs_nldi": dict(
        doi=None, verified=False,
        text="U.S. Geological Survey. Network Linked Data Index (NLDI), navigating the NHDPlus "
             "v2.1 medium-resolution flowline network. https://api.water.usgs.gov/nldi/",
        note="Used 2026-07-09 to fetch each pair's river centreline, so that an OpenStreetMap "
             "structure can be tested for sitting ON the river rather than merely near it."),
    "osm_overpass": dict(
        doi=None, verified=False,
        text="OpenStreetMap contributors. Dam, weir and lock_gate features queried through the "
             "Overpass API. ODbL. https://overpass-api.de/",
        note="Queried 2026-07-09 over a window straddling each gauge pair. OpenStreetMap is a "
             "volunteered inventory, not an authoritative dam register, so an absent structure "
             "is weaker evidence than a present one. See the limitations section."),
}


def cite(*keys: str) -> str:
    """Render a reference block for a notebook cell. Raises on an unknown key so a
    fabricated citation cannot silently reach the notebook."""
    out = []
    for k in keys:
        if k not in REFERENCES:
            raise KeyError(f"citation key {k!r} is not in REFERENCES; refusing to invent one")
        r = REFERENCES[k]
        tag = f"doi:{r['doi']}" if r["doi"] else "no DOI"
        out.append(f"  [{k}] {r['text']}  ({tag})")
    return "\n".join(out)


# --------------------------------------------------------------------------------------
# Cached USGS NWIS access. Every network response lands in tvslope_src/sebastian/sq_cache/ as CSV, so
# the whole section re-runs offline and headless.
# --------------------------------------------------------------------------------------
_SITE: dict[str, dict] = {}


def site_info(g: str, refresh: bool = False) -> dict:
    """Station metadata: name, decimal lat/lon, gauge datum (m), datum accuracy (m),
    vertical datum code. Mirrors per_reach3.datum, which uses alt_va * FT."""
    if not refresh and g in _SITE:
        return _SITE[g]
    f = CACHE / f"site_{g}.csv"
    if f.exists() and not refresh:
        _SITE[g] = pd.read_csv(f, dtype={"site_no": str}).iloc[0].to_dict()
        return _SITE[g]
    url = "https://waterservices.usgs.gov/nwis/site/?" + urllib.parse.urlencode(
        {"format": "rdb", "sites": g, "siteOutput": "expanded"})
    last = None
    for attempt in range(4):
        try:
            raw = urllib.request.urlopen(url, timeout=90).read().decode()
            break
        except Exception as exc:                       # noqa: BLE001
            last = exc
            time.sleep(5 * (attempt + 1))
    else:
        raise RuntimeError(f"NWIS site service failed for {g} after 4 attempts: {last}")
    rows = [ln for ln in raw.splitlines() if ln and not ln.startswith("#")]
    d = dict(zip(rows[0].split("\t"), rows[2].split("\t")))

    def _f(key):
        try:
            return float(d[key])
        except (KeyError, ValueError):
            return np.nan

    rec = dict(site_no=g, name=d["station_nm"].strip(),
               lat=_f("dec_lat_va"), lon=_f("dec_long_va"),
               alt_m=_f("alt_va") * FT, alt_acy_m=abs(_f("alt_acy_va")) * FT,
               vdatum=d.get("alt_datum_cd", "").strip(),
               hdatum=d.get("dec_coord_datum_cd", "").strip())
    pd.DataFrame([rec]).to_csv(f, index=False)
    _SITE[g] = rec
    return rec


def dv(g: str, pcode: str, start: str, refresh: bool = False) -> pd.DataFrame:
    """Daily values for one parameter code. 00065 = gauge height (ft), 00060 = discharge (cfs).
    Returns columns [date, v] in NATIVE units; callers apply FT / CFS."""
    f = CACHE / f"dv_{g}_{pcode}.csv"
    if f.exists() and not refresh:
        return pd.read_csv(f, parse_dates=["date"])
    import dataretrieval.nwis as nwis
    df, _ = nwis.get_dv(sites=g, parameterCd=[pcode], start=start, end="2026-07-01")
    df = df.reset_index()
    col = next((c for c in df.columns if c.startswith(pcode) and c.endswith("_Mean")), None)
    out = pd.DataFrame({
        "date": pd.to_datetime(df["datetime"]).dt.tz_localize(None),
        "v": pd.to_numeric(df[col], errors="coerce") if col else np.nan,
    }).dropna(subset=["v"])
    out.to_csv(f, index=False)
    return out


def span_m(gup: str, gdn: str) -> float:
    """Great-circle gauge separation, metres. Same haversine and same Earth radius as
    final_config._gauge_span_km, so spans match the production code exactly."""
    a, b = site_info(gup), site_info(gdn)
    p1, p2 = np.radians(a["lat"]), np.radians(b["lat"])
    dphi = np.radians(b["lat"] - a["lat"])
    dlmb = np.radians(b["lon"] - a["lon"])
    h = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return float(2 * R_EARTH_KM * np.arcsin(np.sqrt(h))) * 1e3


# --------------------------------------------------------------------------------------
# The twin-gauge chain.
# --------------------------------------------------------------------------------------
def xgauge(site: str, refresh: bool = False) -> pd.DataFrame:
    """Water-surface elevation (m) and discharge (m3/s) for a cross-site gauge.

    Reads `sq_cache/xg_{site}.csv`, carried over from NB_USGS_Gauges_Slope's own cache so the
    numbers here are identical to that notebook's. If the file is missing, pulls live and
    reproduces that notebook's `get()`: daily values first, and where a site has NO daily
    gage-height record, instantaneous stage resampled to a daily median. Station 03353611 is
    exactly that case, so a naive daily-only pull would silently return a different series.
    """
    f = CACHE / f"xg_{site}.csv"
    if f.exists() and not refresh:
        return pd.read_csv(f, index_col=0, parse_dates=True)

    import dataretrieval.nwis as nwis
    info, _ = nwis.get_info(sites=site)
    alt_ft = float(info.alt_va.iloc[0]) if pd.notna(info.get("alt_va", pd.Series([np.nan])).iloc[0]) else np.nan
    off = alt_ft * FT if np.isfinite(alt_ft) else 0.0

    dv_, _ = nwis.get_dv(sites=site, parameterCd="00060,00065", start="2010-01-01", end="2024-12-31")
    gh = [c for c in dv_.columns if "00065" in c and "cd" not in c]
    q = [c for c in dv_.columns if "00060" in c and "cd" not in c]
    if gh:
        out = pd.DataFrame(index=dv_.index)
        out["wse"] = dv_[gh[0]].astype(float) * FT + off
        out["Q"] = dv_[q[0]].astype(float) * CFS if q else np.nan
    else:                                        # no daily stage: instantaneous, daily median
        iv, _ = nwis.get_iv(sites=site, parameterCd="00060,00065", start="2018-01-01", end="2024-12-31")
        ivgh = [c for c in iv.columns if "00065" in c and "cd" not in c]
        ivq = [c for c in iv.columns if "00060" in c and "cd" not in c]
        out = pd.DataFrame({"wse": iv[ivgh[0]].astype(float).resample("D").median() * FT + off})
        if ivq:
            out["Q"] = iv[ivq[0]].astype(float).resample("D").median() * CFS
        elif q and len(dv_):
            out = out.join((dv_[q[0]].astype(float) * CFS).rename("Q"))
        else:
            out["Q"] = np.nan
    out.to_csv(f)
    return out


def reach_span_m(reach: str) -> float:
    """Gauge separation in metres. Cross-site reaches carry an explicit along-channel span;
    the FIM reaches use the great-circle distance, matching final_config._gauge_span_km."""
    cfg = ALL_REACHES[reach]
    if cfg.get("span_m") is not None:
        return float(cfg["span_m"])
    return span_m(cfg["gup"], cfg["gdn"])


def have_xgauge(site: str) -> bool:
    """True when a cross-site gauge is cached locally. Guards against `xgauge` silently firing a
    live NWIS pull for a drainage-area donor that was never carried into this repo."""
    return bool(site) and (CACHE / f"xg_{site}.csv").exists()


def _reach_discharge(cfg: dict, m: pd.DataFrame) -> tuple[pd.Series, str]:
    """On-reach discharge for a cross-site pair, and a plain-English record of where it came from.

    Three provenances, in descending order of trust:
      pair gauge   one of the two stage stations also gauges discharge.
      third gauge  a third station on the SAME SWORD reach gauges it. Still an on-reach measurement.
      transferred  a donor gauge elsewhere, scaled by a drainage-area ratio. This is a MODEL of the
                   reach's discharge, not a measurement of it, so Step 7 refuses to fit S(Q) to it.
    """
    q = m["Qd"].where(m["Qd"].notna(), m["Qu"])
    src = cfg.get("q_source", "pair gauge")
    if q.notna().sum() > 0 and src == "pair gauge":
        return q, "pair gauge"
    gq = cfg.get("gq")
    if src == "third gauge" and gq and have_xgauge(gq):
        return xgauge(gq).Q.reindex(m.index), f"third gauge {gq} on the same reach"
    if src == "transferred":
        donor, ratio = cfg.get("donor"), float(cfg.get("da_ratio") or 1.0)
        if donor and have_xgauge(donor):
            return xgauge(donor).Q.reindex(m.index) * ratio, f"drainage-area transfer from {donor} (DA {ratio:.3f})"
        return pd.Series(np.nan, index=m.index), f"drainage-area transfer from {donor}, donor NOT cached here"
    return q, "pair gauge"


def _xtwin(reach: str, clip_q) -> pd.DataFrame:
    """twin_series for a cross-site reach, reproducing NB_USGS_Gauges_Slope.slope_series:
    concat the two water-level series, take discharge from the downstream gauge and fall back
    to the upstream, and re-order the pair by median water level if they are the wrong way up."""
    cfg = XREACHES[reach]
    L = reach_span_m(reach)
    du, dd = xgauge(cfg["gup"]), xgauge(cfg["gdn"])
    m = pd.concat([du.wse.rename("wu"), dd.wse.rename("wd"),
                   du.Q.rename("Qu"), dd.Q.rename("Qd")], axis=1).dropna(subset=["wu", "wd"])
    swapped = bool(m.wu.median() < m.wd.median())
    if swapped:
        m = m.rename(columns={"wu": "wd", "wd": "wu", "Qu": "Qd", "Qd": "Qu"})
    m["discharge_cms"], q_origin = _reach_discharge(cfg, m)
    m["S"] = (m.wu - m.wd) / L
    n_raw = len(m)
    qual = _pair_quality_from(m, cfg)          # computed on the RAW series, before any clip
    if len(m) > 20:
        lo, hi = m.S.quantile(list(clip_q))
        m = m[m.S.between(lo, hi)]
    m = m.reset_index().rename(columns={m.index.name or "index": "date"})
    up, dn = site_info(cfg["gup"]), site_info(cfg["gdn"])
    m.attrs.update(reach=reach, span_m=L, n_raw=n_raw, swapped=swapped, q_origin=q_origin,
                   vdatum_up=up["vdatum"], vdatum_dn=dn["vdatum"],
                   vdatum_mismatch=up["vdatum"] != dn["vdatum"], **qual)
    return m


def _pair_quality_from(m: pd.DataFrame, cfg: dict) -> dict:
    """The two selection statistics NB_USGS_Gauges_Slope cell 25 uses, recomputed here.

        signal_to_datum = |median(wse_up - wse_dn)| / (alt_acy_up + alt_acy_dn)
        frac_neg        = share of days on which the water surface runs UPHILL, S <= 0

    and its verdict, verbatim: single_slope_valid = (signal_to_datum > 3) & (frac_neg < 0.10).
    A pair failing frac_neg does not have a noisy slope. It has no single slope at all.
    """
    up, dn = site_info(cfg["gup"]), site_info(cfg["gdn"])
    acy = float(np.nansum([up["alt_acy_m"], dn["alt_acy_m"]]))
    drop = float(np.abs((m.wu - m.wd).median()))
    s2d = drop / acy if acy > 0 else np.nan
    fneg = float((m.S <= 0).mean())
    return dict(wse_drop_m=drop, datum_acy_sum_m=acy, signal_to_datum=s2d, frac_neg=fneg,
                single_slope_valid=bool(np.isfinite(s2d)
                                        and s2d > PROVENANCE["SIGNAL_TO_DATUM_MIN"]["value"]
                                        and fneg < PROVENANCE["FRAC_NEG_MAX"]["value"]))


def twin_series(reach: str, clip_q=PROVENANCE["SLOPE_CLIP_Q"]["value"]) -> pd.DataFrame:
    """Daily twin-gauge slope S(t) = (wse_up - wse_dn)/L with on-reach discharge Q(t).

    Mirrors per_reach3.twin_series, including the n>20 quantile clip on S. WSE is the
    gauge datum plus the recorded gauge height, exactly as per_reach3.wse_series does.

    NOTE. per_reach3 adds alt_va to gauge height with no vertical-datum conversion. Where
    the two stations report different alt_datum_cd values, S carries a constant offset.
    Section 7.2 quantifies this. `vdatum_mismatch` in the returned attrs flags it.
    """
    if reach in XREACHES:
        return _xtwin(reach, clip_q)
    cfg = REACHES[reach]
    L = reach_span_m(reach)
    up, dn = site_info(cfg["gup"]), site_info(cfg["gdn"])

    su = dv(cfg["gup"], "00065", "2015-01-01")
    sd = dv(cfg["gdn"], "00065", "2015-01-01")
    u = pd.DataFrame({"date": su.date, "wu": up["alt_m"] + su.v.values * FT})
    d = pd.DataFrame({"date": sd.date, "wd": dn["alt_m"] + sd.v.values * FT})

    m = u.merge(d, on="date")
    m["S"] = (m.wu - m.wd) / L
    n_raw = len(m)
    qual = _pair_quality_from(m, cfg)          # on the RAW series, before the quantile clip
    if len(m) > 20:
        lo, hi = m.S.quantile(list(clip_q))
        m = m[m.S.between(lo, hi)]

    q = dv(cfg["gq"], "00060", "2010-01-01")
    q = pd.DataFrame({"date": q.date, "discharge_cms": q.v.values * CFS})
    m = m.merge(q, on="date", how="left").sort_values("date").reset_index(drop=True)

    m.attrs.update(reach=reach, span_m=L, n_raw=n_raw, swapped=False,
                   q_origin=f"pair gauge {cfg['gq']}",
                   vdatum_up=up["vdatum"], vdatum_dn=dn["vdatum"],
                   vdatum_mismatch=up["vdatum"] != dn["vdatum"], **qual)
    return m


def sq_pairs(reach: str, mad_k=PROVENANCE["MAD_K"]["value"],
             min_n=PROVENANCE["MIN_N"]["value"], tw: pd.DataFrame | None = None,
             positivity: bool = True) -> pd.DataFrame | None:
    """Quality-controlled (Q, S) cloud. Verbatim port of timevarying_slope.sq_pairs."""
    tw = twin_series(reach) if tw is None else tw
    d = tw.dropna(subset=["S", "discharge_cms"]).copy()
    if positivity:
        d = d[(d.discharge_cms > 0) & (d.S > 0)]
    if len(d) < min_n:
        return None
    scale = PROVENANCE["MAD_SCALE"]["value"]
    for c in ["S", "discharge_cms"]:
        x = np.log(d[c].values)
        med = np.median(x)
        mad = np.median(np.abs(x - med)) or 1e-9
        d = d[np.abs(np.log(d[c].values) - med) <= mad_k * scale * mad]
    if len(d) < min_n:
        return None
    out = d[["discharge_cms", "S"]].rename(columns={"discharge_cms": "Q_cms"}).reset_index(drop=True)
    out.attrs.update(tw.attrs)
    return out


# --------------------------------------------------------------------------------------
# Fitting. Verbatim ports of timevarying_slope._fit_quadratic / _fit_powerlaw / fit_sq.
# --------------------------------------------------------------------------------------
def fit_quadratic(Q, S) -> dict:
    c = np.polyfit(Q, S, 2)
    f = lambda q, c=c: np.clip(np.polyval(c, np.asarray(q, float)), 1e-7, None)  # noqa: E731
    r2 = 1 - np.sum((S - f(Q)) ** 2) / max(np.sum((S - S.mean()) ** 2), 1e-12)
    return dict(func=f, kind="quadratic", r2=float(r2), params=[float(v) for v in c])


def fit_powerlaw(Q, S) -> dict:
    (a, b, cc), _ = curve_fit(lambda q, a, b, cc: a * np.power(q, b) + cc, Q, S,
                              p0=[np.median(S), 0.3, 0.0], maxfev=10000)
    f = lambda q, a=a, b=b, cc=cc: np.clip(a * np.power(np.asarray(q, float), b) + cc, 1e-7, None)  # noqa: E731
    r2 = 1 - np.sum((S - f(Q)) ** 2) / max(np.sum((S - S.mean()) ** 2), 1e-12)
    return dict(func=f, kind="powerlaw", r2=float(r2), params=[float(a), float(b), float(cc)])


def fit_sq(Q, S) -> dict | None:
    """Keep the better of quadratic and power-law by R2 alone. This is what the production
    code does. R2 does not penalise parameters, but both candidates have three, so the
    comparison is fair here. Section 7.6 reports AIC as a cross-check."""
    Q, S = np.asarray(Q, float), np.asarray(S, float)
    cands = []
    for fn in (fit_quadratic, fit_powerlaw):
        try:
            cands.append(fn(Q, S))
        except Exception:                              # noqa: BLE001
            pass
    if not cands:
        return None
    best = max(cands, key=lambda d: d["r2"])
    best["n"] = int(len(Q))
    best["Q_range"] = (float(np.min(Q)), float(np.max(Q)))
    best["S_range"] = (float(np.min(S)), float(np.max(S)))
    best["all_r2"] = {c["kind"]: c["r2"] for c in cands}
    resid = S - best["func"](Q)
    k = len(best["params"])
    best["rmse"] = float(np.sqrt(np.mean(resid ** 2)))
    best["nse"] = float(1 - np.sum(resid ** 2) / np.sum((S - S.mean()) ** 2))
    best["aic"] = float(len(Q) * np.log(np.mean(resid ** 2)) + 2 * k)
    for c in cands:
        r = S - c["func"](Q)
        c["aic"] = float(len(Q) * np.log(np.mean(r ** 2)) + 2 * len(c["params"]))
    best["all_aic"] = {c["kind"]: c["aic"] for c in cands}
    return best


# --------------------------------------------------------------------------------------
# Locator-map support. Deliberately avoids cartopy and contextily: the notebook's kernel is
# `fimserve`, and neither package is guaranteed there. A slippy-map tile is fetched once
# with urllib, stitched with PIL (a matplotlib dependency), and cached as PNG in sq_cache/.
# Plotting happens in Web Mercator metres so the imagery is not distorted.
# --------------------------------------------------------------------------------------
MERC_R = 6378137.0                       # WGS84 semi-major axis, the Web Mercator sphere radius
MERC_A = np.pi * MERC_R                  # 20037508.342789244 m, half the world extent
TILE_URL = ("https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}")
TILE_ATTR = "Imagery: Esri World Imagery (Esri, Maxar, Earthstar Geographics)"


def lonlat_to_merc(lon, lat):
    """WGS84 lon/lat (degrees) to Web Mercator (EPSG:3857) metres."""
    lon, lat = np.asarray(lon, float), np.asarray(lat, float)
    x = np.radians(lon) * MERC_R
    y = MERC_R * np.log(np.tan(np.pi / 4 + np.radians(lat) / 2))
    return x, y


def merc_to_lonlat(x, y):
    """Web Mercator (EPSG:3857) metres back to WGS84 lon/lat degrees."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    lon = np.degrees(x / MERC_R)
    lat = np.degrees(2 * np.arctan(np.exp(y / MERC_R)) - np.pi / 2)
    return lon, lat


def map_box(lons, lats, aspect=1.25, pad_frac=0.55):
    """A Web Mercator view box containing every point, padded, at a FIXED width/height
    aspect. Forcing one aspect across reaches keeps the locator panels the same shape even
    though one gauge pair runs north-south and the other runs east-west."""
    xs, ys = lonlat_to_merc(np.asarray(lons), np.asarray(lats))
    cx, cy = 0.5 * (xs.min() + xs.max()), 0.5 * (ys.min() + ys.max())
    half = 0.5 * max(xs.max() - xs.min(), ys.max() - ys.min()) * (1 + pad_frac)
    half = max(half, 400.0)
    hx, hy = half * aspect, half
    return cx - hx, cx + hx, cy - hy, cy + hy


def _tile_xy(lon, lat, z):
    """Fractional slippy-map tile index."""
    n = 2 ** z
    xt = (lon + 180.0) / 360.0 * n
    lat_r = np.radians(lat)
    yt = (1.0 - np.log(np.tan(lat_r) + 1.0 / np.cos(lat_r)) / np.pi) / 2.0 * n
    return xt, yt


def _tile_merc_extent(i, j, z):
    """Web Mercator bounds (xmin, xmax, ymin, ymax) of tile (i, j) at zoom z."""
    n = 2 ** z
    s = 2 * MERC_A / n
    return (-MERC_A + i * s, -MERC_A + (i + 1) * s,
            MERC_A - (j + 1) * s, MERC_A - j * s)


def fetch_basemap(lon0, lat0, lon1, lat1, pad_frac=0.35, max_tiles=16):
    """Stitch an imagery basemap covering the given lon/lat box, padded.

    Returns (image_array, extent) where extent is (xmin, xmax, ymin, ymax) in Web Mercator
    metres, ready for `ax.imshow(img, extent=extent, origin='upper')`.

    The stitched result is cached, so this touches the network at most once per view.
    """
    from PIL import Image

    dlon, dlat = abs(lon1 - lon0), abs(lat1 - lat0)
    lo_lon, hi_lon = min(lon0, lon1) - pad_frac * dlon, max(lon0, lon1) + pad_frac * dlon
    lo_lat, hi_lat = min(lat0, lat1) - pad_frac * dlat, max(lat0, lat1) + pad_frac * dlat

    # Pick the deepest zoom whose tile count stays under max_tiles.
    zoom = 10
    for z in range(18, 9, -1):
        x0, y0 = _tile_xy(lo_lon, hi_lat, z)
        x1, y1 = _tile_xy(hi_lon, lo_lat, z)
        if (int(x1) - int(x0) + 1) * (int(y1) - int(y0) + 1) <= max_tiles:
            zoom = z
            break

    x0, y0 = _tile_xy(lo_lon, hi_lat, zoom)
    x1, y1 = _tile_xy(hi_lon, lo_lat, zoom)
    i0, i1, j0, j1 = int(x0), int(x1), int(y0), int(y1)

    key = f"basemap_z{zoom}_{i0}-{i1}_{j0}-{j1}.png"
    cached = CACHE / key
    if cached.exists():
        img = np.asarray(Image.open(cached))
    else:
        cols, rows = i1 - i0 + 1, j1 - j0 + 1
        canvas = Image.new("RGB", (256 * cols, 256 * rows))
        for i in range(i0, i1 + 1):
            for j in range(j0, j1 + 1):
                url = TILE_URL.format(z=zoom, x=i, y=j)
                req = urllib.request.Request(
                    url, headers={"User-Agent": "SebastianMarshall-research/1.0"})
                last = None
                for attempt in range(3):
                    try:
                        with urllib.request.urlopen(req, timeout=60) as r:
                            tile = Image.open(r).convert("RGB")
                        break
                    except Exception as exc:                # noqa: BLE001
                        last = exc
                        time.sleep(2 * (attempt + 1))
                else:
                    raise RuntimeError(f"tile {zoom}/{i}/{j} failed: {last}")
                canvas.paste(tile, ((i - i0) * 256, (j - j0) * 256))
        canvas.save(cached)
        img = np.asarray(canvas)

    xa, _, _, yb = _tile_merc_extent(i0, j0, zoom)
    _, xb, ya, _ = _tile_merc_extent(i1, j1, zoom)
    return img, (xa, xb, ya, yb)


def merc_scale(lat):
    """Web Mercator inflates distance by 1/cos(lat). Multiply a ground distance by this to
    get its length in Mercator metres, so a scale bar is drawn true."""
    return 1.0 / np.cos(np.radians(lat))


def solve_Q(q_orig, s_old, sfunc, q_lo, q_hi, iters=60, tol=1e-4):
    """Verbatim port of timevarying_slope._solve_Q. Solve Q = q_orig * sqrt(S(Q)/s_old) by
    damped fixed-point iteration, with S evaluated only inside the fitted Q support.

    The clamp `qc = clip(q, q_lo, q_hi)` is the line that matters: any hydroTable row whose
    iterated discharge exceeds q_hi silently reads S(q_hi) instead of S at its own discharge.
    """
    q = float(q_orig)
    for _ in range(iters):
        qc = min(max(q, q_lo), q_hi)
        s_new = float(sfunc(qc))
        q2 = q_orig * np.sqrt(max(s_new, 1e-9) / max(s_old, 1e-9))
        if abs(q2 - q) <= tol * max(q2, 1.0):
            q = q2
            break
        q = 0.5 * (q + q2)
    return q, float(sfunc(min(max(q, q_lo), q_hi)))


# --------------------------------------------------------------------------------------
# Diagnostics that the production code does not provide.
# --------------------------------------------------------------------------------------
def sigma_S(reach: str, sigma_h: float = PROVENANCE["SIGMA_H_M"]["value"]) -> float:
    """Random precision floor of the twin-gauge slope, m/m.

    Two independent stage readings, each with standard error sigma_h, differenced over a
    span L, give sigma_S = sqrt(2) * sigma_h / L. Slopes below roughly 2 sigma_S are not
    distinguishable from a flat water surface.
    """
    return float(np.sqrt(2) * sigma_h / reach_span_m(reach))


def datum_bias_S(reach: str) -> float:
    """Systematic slope bias, m/m, implied by the two published gauge-datum accuracies
    (NWIS alt_acy_va), combined in quadrature. Unlike sigma_S this is a CONSTANT offset:
    it moves the fitted intercept only, leaving dS/dQ and the vertex untouched."""
    cfg = ALL_REACHES[reach]
    a = site_info(cfg["gup"])["alt_acy_m"]
    b = site_info(cfg["gdn"])["alt_acy_m"]
    return float(np.sqrt(np.nansum(np.array([a, b]) ** 2)) / reach_span_m(reach))


def bootstrap_params(Q, S, kind: str, B: int = 500, seed: int = 20260709) -> np.ndarray:
    """Nonparametric bootstrap over the (Q,S) cloud. Returns a (B', n_params) array."""
    rng = np.random.default_rng(seed)
    fn = fit_powerlaw if kind == "powerlaw" else fit_quadratic
    Q, S = np.asarray(Q, float), np.asarray(S, float)
    out = []
    for _ in range(B):
        i = rng.integers(0, len(Q), len(Q))
        try:
            out.append(fn(Q[i], S[i])["params"])
        except Exception:                              # noqa: BLE001
            pass
    return np.asarray(out)


def curve_shape(fit: dict) -> dict:
    """Where the fitted curve misbehaves.

    quadratic: vertex Q* = -c1/(2 c2). c2 > 0 means a convex curve with a MINIMUM, so S
               turns back upward beyond Q*. c2 < 0 means concave with a maximum.
    powerlaw:  if the additive constant c < 0, the curve crosses S = 0 at
               Q0 = (-c/a)^(1/b). Inside the observed support, np.clip hides a negative
               predicted slope.
    """
    out = dict(kind=fit["kind"])
    q_lo, q_hi = fit["Q_range"]
    if fit["kind"] == "quadratic":
        c2, c1, _ = fit["params"]
        qv = -c1 / (2 * c2)
        out.update(vertex_Q=float(qv), convex=bool(c2 > 0),
                   vertex_inside_support=bool(q_lo <= qv <= q_hi))
    else:
        a, b, c = fit["params"]
        if c < 0 < a:
            q0 = float((-c / a) ** (1.0 / b))
            out.update(zero_crossing_Q=q0, zero_inside_support=bool(q_lo <= q0 <= q_hi))
        else:
            out.update(zero_crossing_Q=None, zero_inside_support=False)
    return out


def sq_equation(fit: dict) -> str:
    """The fitted relation in FIGURE units: S in mm/km, Q in m3/s."""
    p = fit["params"]
    if fit["kind"] == "quadratic":
        c2, c1, c0 = [v * MM_PER_KM for v in p]
        return f"S(Q) = {c2:.2e}·Q² {c1:+.2e}·Q {c0:+.1f}"
    a, b, c = p
    return f"S(Q) = {a*MM_PER_KM:.2f}·Q$^{{{b:.2f}}}$ {c*MM_PER_KM:+.1f}"


# --------------------------------------------------------------------------------------
# Fidelity check against the fits printed in the notebook's own Step 6 output.
# --------------------------------------------------------------------------------------
PUBLISHED = {
    "74282100101": dict(kind="powerlaw", params=[9.38e-06, 0.26, -3.01e-05], r2=0.89),
    "74267300251": dict(kind="quadratic", params=[1.41e-11, -4.35e-07, 3.84e-03], r2=0.99),
}


def verify_against_notebook(rtol: float = 0.05) -> pd.DataFrame:
    """Confirm sq_core reproduces the fits that Step 6 printed from timevarying_slope.
    Returns one row per reach with the published value, the recomputed value, and a PASS flag."""
    rows = []
    for reach, pub in PUBLISHED.items():
        f = fit_sq(*[sq_pairs(reach)[c].values for c in ("Q_cms", "S")])
        ok_kind = f["kind"] == pub["kind"]
        ok_r2 = abs(f["r2"] - pub["r2"]) < 0.01
        ok_par = all(np.isclose(a, b, rtol=rtol, atol=1e-12)
                     for a, b in zip(f["params"], pub["params"]))
        rows.append(dict(reach=reach, river=REACHES[reach]["river"],
                         kind_pub=pub["kind"], kind_new=f["kind"],
                         r2_pub=pub["r2"], r2_new=round(f["r2"], 4), n=f["n"],
                         params_pub=[f"{v:.3g}" for v in pub["params"]],
                         params_new=[f"{v:.3g}" for v in f["params"]],
                         PASS=bool(ok_kind and ok_r2 and ok_par)))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 200)
    print(verify_against_notebook().to_string(index=False))


# --------------------------------------------------------------------------------------
# The Step 7 panel figure: one column per gauge pair, three rows (locator map, S(Q),
# stage-discharge). Lives here rather than in the notebook so the section can render the
# open-channel pairs and the structure-affected pairs as two separate figures from one
# code path. Each notebook cell still produces exactly one figure.
# --------------------------------------------------------------------------------------
IRIS_STATIC = {"74282100101": 19.4, "74267300251": 35.7}   # mm/km, Step 6 slope_treatments table

# Hand-placed label offsets (points) so no annotation covers a marker or another label.
MAP_LABEL_OFFSETS = {
    "74282100101": dict(up=(0, 30), dn=(38, -6), dam=(0, 0)),
    "73260900321": dict(up=(0, 30), dn=(46, 0), dam=(0, 0)),
    "74266400321": dict(up=(0, 30), dn=(0, 36), dam=(96, 2)),
    "74267300251": dict(up=(30, -26), dn=(4, 40), dam=(0, -46)),
}
C_PT, C_FIT, C_IRIS = "#8e44ad", "#c0392b", "#0f6fb5"
C_UP, C_DN, C_DAM, C_SUP, C_NOISE = "#00b0f0", "#ffd166", "#ff2d2d", "#2ecc71", "#95a5a6"


# --------------------------------------------------------------------------------------
# The candidate ledger: which of the 12 gauge pairs Step 7 may fit, and why the rest fail.
#
# Every gate is COMPUTED from the cached series. None is copied from the source notebook's
# result CSVs. The gate definitions themselves are traced to NB_USGS_Gauges_Slope cell 25.
# --------------------------------------------------------------------------------------
GATES = [
    ("G1 pair + span",      "two stage gauges with an along-channel separation"),
    ("G2 on-reach Q",       "discharge measured on this reach, not drainage-area transferred"),
    ("G3 head > 3x datum",  f"signal_to_datum > {PROVENANCE['SIGNAL_TO_DATUM_MIN']['value']:g}"),
    ("G4 few uphill days",  f"frac_neg < {PROVENANCE['FRAC_NEG_MAX']['value']:g}"),
    ("G5 n >= min_n",       f"at least {PROVENANCE['MIN_N']['value']} (Q,S) pairs survive the QC ladder"),
]


def candidate_ledger() -> pd.DataFrame:
    """One row per candidate pair, one column per gate, plus the fit where a fit is allowed.

    `sword_reach` records whether the pair sits on a SWORD reach. The five self-found pairs do not,
    so they can never carry a SWOT slope, however good their gauge record is. That is a constraint
    on the SWOT comparison, not on this section.
    """
    rows = []
    for reach, cfg in ALL_REACHES.items():
        r = dict(reach=reach, river=cfg["river"],
                 role=("FIM reach" if reach in REACHES else f"cross-site ({cfg.get('status','-')})"),
                 gauge_up=cfg["gup"], gauge_dn=cfg["gdn"],
                 L_km=reach_span_m(reach) / 1000.0,
                 sword_reach=("yes" if reach.isdigit() else "no"),
                 q_source=cfg.get("q_source", "pair gauge"))
        try:
            tw = twin_series(reach)
        except Exception as e:                                   # noqa: BLE001
            r.update(gate_fail=f"series unavailable: {e}"); rows.append(r); continue

        a = tw.attrs
        r.update(n_raw=a["n_raw"], wse_drop_m=a["wse_drop_m"], datum_acy_sum_m=a["datum_acy_sum_m"],
                 signal_to_datum=a["signal_to_datum"], frac_neg=a["frac_neg"],
                 q_origin=a.get("q_origin", "pair gauge"),
                 datum_ok=not a["vdatum_mismatch"])

        r["G1 pair + span"] = True
        r["G2 on-reach Q"] = r["q_source"] in ("pair gauge", "third gauge")
        r["G3 head > 3x datum"] = bool(a["signal_to_datum"] > PROVENANCE["SIGNAL_TO_DATUM_MIN"]["value"])
        r["G4 few uphill days"] = bool(a["frac_neg"] < PROVENANCE["FRAC_NEG_MAX"]["value"])

        p = sq_pairs(reach, tw=tw) if tw.discharge_cms.notna().any() else None
        r["n_fit"] = 0 if p is None else len(p)
        r["G5 n >= min_n"] = bool(r["n_fit"] >= PROVENANCE["MIN_N"]["value"])

        r["eligible"] = all(bool(r[g]) for g, _ in GATES)
        r["gate_fail"] = "" if r["eligible"] else ", ".join(g for g, _ in GATES if not r[g])

        if r["eligible"] and p is not None:
            Q, S = p.Q_cms.values, p.S.values
            f = fit_sq(Q, S)
            trend, dS = reach_trend(reach, f)
            r.update(kind=f["kind"], r2=f["r2"], dSdQ=dS * MM_PER_KM, trend=trend,
                     S_med=float(np.median(S)) * MM_PER_KM,
                     S_range=(float(S.max()) - float(S.min())) * MM_PER_KM,
                     informative=bool(f["r2"] >= PROVENANCE["R2_FLOOR"]["value"]))
        else:
            r.update(kind=None, r2=np.nan, dSdQ=np.nan, trend=None, S_med=np.nan,
                     S_range=np.nan, informative=False)

        st = STRUCTURES_ON_RIVER.get(reach, [])
        r["n_on_river"] = len(st)
        r["structures"] = "; ".join(f"{s['name']} ({s['dist_m']} m)" for s in st) or "none on the centreline"
        rows.append(r)
    return pd.DataFrame(rows)


def eligible_reaches() -> list[str]:
    """The reaches Step 7 is allowed to fit an S(Q) curve to, in ledger order."""
    led = candidate_ledger()
    return list(led[led.eligible].reach)


def bootstrap_dSdQ(reach: str, B: int = 600, seed: int = 20260709) -> tuple:
    """Bootstrap the SIGN of dS/dQ at the median discharge. Returns (dSdQ, lo, hi) in mm/km per m3/s."""
    p = sq_pairs(reach)
    Q, S = p.Q_cms.values, p.S.values
    f = fit_sq(Q, S)
    q50 = float(np.median(Q))
    Bp = bootstrap_params(Q, S, f["kind"], B=B, seed=seed)
    d = ((2 * Bp[:, 0] * q50 + Bp[:, 1]) if f["kind"] == "quadratic"
         else Bp[:, 0] * Bp[:, 1] * q50 ** (Bp[:, 1] - 1)) * MM_PER_KM
    lo, hi = (float(v) for v in np.percentile(d, [2.5, 97.5]))
    return reach_trend(reach, f)[1] * MM_PER_KM, lo, hi


def reach_trend(reach, f=None):
    """Sign of dS/dQ at the median discharge, computed from the fit. Returns (word, value)."""
    p = sq_pairs(reach)
    f = f or fit_sq(p.Q_cms.values, p.S.values)
    q50 = float(np.median(p.Q_cms.values))
    a = f["params"]
    d = (2 * a[0] * q50 + a[1]) if f["kind"] == "quadratic" else a[0] * a[1] * q50 ** (a[1] - 1)
    return ("rises" if d > 0 else "falls"), float(d)


def panel_figure(reaches, suptitle, subtitle, out_png=None, dpi=125):
    """Build the three-row panel figure for the given reaches. Returns (fig, facts)."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D

    N = len(reaches)
    LET = "abcdefghijklmnop"
    fig, axs = plt.subplots(3, N, figsize=(7.9 * N, 18.4),
                            gridspec_kw=dict(height_ratios=[1.0, 1.0, 1.0],
                                             hspace=0.26, wspace=0.235))
    axs = np.atleast_2d(axs)
    if N == 1:
        axs = axs.reshape(3, 1)
    facts = []

    for col, reach in enumerate(reaches):
        cfg = ALL_REACHES[reach]
        up, dn = site_info(cfg["gup"]), site_info(cfg["gdn"])
        L_m = reach_span_m(reach)
        tw = twin_series(reach)
        p = sq_pairs(reach, tw=tw)
        Q, S = p.Q_cms.values, p.S.values
        f = fit_sq(Q, S); shape = curve_shape(f); par = f["params"]
        lm_list = LANDMARKS.get(reach, [])
        q_fl = cfg.get("q_flood_cms")
        s_static = IRIS_STATIC.get(reach)
        is_fim = reach in REACHES
        off_map = MAP_LABEL_OFFSETS[reach]

        trend, dS = reach_trend(reach, f)
        facts.append(dict(reach=reach, river=cfg["river"], trend=trend, kind=f["kind"],
                          c2=par[0], S_med=float(np.median(S)) * MM_PER_KM,
                          struct=(lm_list[0]["name"] if lm_list else "no mapped structure")))

        # ---- row 1: locator map ------------------------------------------------------
        ax = axs[0, col]
        # Match the map to the exact width of the plot columns below it: use this cell's own
        # width/height ratio as the view-box aspect, so the equal-aspect map fills the column
        # (no side whitespace, no distortion; the basemap is fetched for this same box).
        _p = ax.get_position()
        cell_aspect = (_p.width * fig.get_figwidth()) / (_p.height * fig.get_figheight())
        lons = [up["lon"], dn["lon"]] + [l["lon"] for l in lm_list]
        lats = [up["lat"], dn["lat"]] + [l["lat"] for l in lm_list]
        bx0, bx1, by0, by1 = map_box(lons, lats, aspect=cell_aspect, pad_frac=0.60)
        lo_lon, lo_lat = merc_to_lonlat(bx0, by0)
        hi_lon, hi_lat = merc_to_lonlat(bx1, by1)
        img, ext = fetch_basemap(float(lo_lon), float(lo_lat), float(hi_lon), float(hi_lat), pad_frac=0.10)
        ax.imshow(img, extent=ext, origin="upper", interpolation="bilinear", zorder=0)
        ax.set_xlim(bx0, bx1); ax.set_ylim(by0, by1)
        ax.set_aspect("equal", adjustable="box")
        ax.grid(False); ax.set_xticks([]); ax.set_yticks([])

        xu, yu = lonlat_to_merc(up["lon"], up["lat"])
        xd, yd = lonlat_to_merc(dn["lon"], dn["lat"])
        ax.plot([xu, xd], [yu, yd], color="white", lw=3.0, ls=(0, (6, 4)), alpha=0.95, zorder=3)
        for x, y, c, mk, tag, sid, off in [(xu, yu, C_UP, "^", "upstream", cfg["gup"], off_map["up"]),
                                           (xd, yd, C_DN, "v", "downstream", cfg["gdn"], off_map["dn"])]:
            ax.plot(x, y, mk, ms=17, mfc=c, mec="black", mew=2.0, zorder=6)
            ha = "left" if off[0] > 0 else ("right" if off[0] < 0 else "center")
            ax.annotate(f"{tag}\n{sid}", (x, y), textcoords="offset points", xytext=off, ha=ha,
                        va="center", fontsize=11.5, fontweight="bold", color="white", zorder=7,
                        bbox=dict(boxstyle="round,pad=0.26", fc="black", ec=c, lw=1.6, alpha=0.82))
        for lm in lm_list:
            xl, yl = lonlat_to_merc(lm["lon"], lm["lat"])
            ax.plot(xl, yl, "X", ms=21, mfc=C_DAM, mec="white", mew=2.2, zorder=8)
            ax.annotate(lm["name"], (xl, yl), textcoords="offset points", xytext=off_map["dam"],
                        ha="center", va="center", fontsize=11.8, fontweight="bold", color="white",
                        zorder=9, bbox=dict(boxstyle="round,pad=0.28", fc=C_DAM, ec="white",
                                            lw=1.6, alpha=0.96))
        if not lm_list:
            ax.text(0.028, 0.175, "no dam / weir / lock mapped\n(OSM Overpass, 2026-07-09)",
                    transform=ax.transAxes, ha="left", va="bottom", fontsize=11.2,
                    fontweight="bold", color="white", zorder=9,
                    bbox=dict(boxstyle="round,pad=0.30", fc="#1e8449", ec="white", lw=1.6, alpha=0.90))

        lat_m = 0.5 * (up["lat"] + dn["lat"])
        bar_km = 0.5 if L_m < 2000 else (1.0 if L_m < 5000 else 2.0)
        bar = bar_km * 1000 * merc_scale(lat_m)
        x_b = bx0 + 0.06 * (bx1 - bx0); y_b = by0 + 0.09 * (by1 - by0)
        ax.plot([x_b, x_b + bar], [y_b, y_b], color="white", lw=5.0, solid_capstyle="butt", zorder=9)
        ax.text(x_b + bar / 2, y_b + 0.021 * (by1 - by0), f"{bar_km:g} km", ha="center",
                fontsize=11.8, fontweight="bold", color="white", zorder=9)
        ax.annotate("N", xy=(0.955, 0.93), xytext=(0.955, 0.80), xycoords="axes fraction",
                    ha="center", fontsize=15.5, fontweight="bold", color="white", zorder=9,
                    arrowprops=dict(arrowstyle="-|>", color="white", lw=2.3))
        ax.text(0.5, 0.045, f"L = {L_m/1000:.3f} km", transform=ax.transAxes, ha="center",
                fontsize=13.5, fontweight="bold", color="white", zorder=9,
                bbox=dict(boxstyle="round,pad=0.30", fc="black", ec="white", lw=1.3, alpha=0.74))
        ax.text(0.5, 0.005, TILE_ATTR, transform=ax.transAxes, ha="center", va="bottom",
                fontsize=7.4, color="white", alpha=0.9, zorder=9)
        dm = "  ·  DATUMS MISMATCHED" if up["vdatum"] != dn["vdatum"] else ""
        tag = "FIM reach" if is_fim else f"cross-site ({cfg.get('status','-')})"
        ax.set_title(f"({LET[col]}) {cfg['river']}  ·  {tag}\n{up['vdatum']} / {dn['vdatum']}{dm}",
                     fontsize=15.5)

        # ---- row 2: S(Q) -------------------------------------------------------------
        ax = axs[1, col]
        Smm = S * MM_PER_KM
        ax.scatter(Q, Smm, s=15, color=C_PT, alpha=0.26, ec="none", zorder=2,
                   label=f"twin-gauge S vs Q  (n={f['n']:,})")
        ql, qh = f["Q_range"]
        ax.axvspan(ql, qh, color=C_SUP, alpha=0.08, zorder=0)
        xf = np.linspace(ql, qh, 400)
        ax.plot(xf, f["func"](xf) * MM_PER_KM, color=C_FIT, lw=3.0, zorder=5,
                label=f"{f['kind']} fit   R² = {f['r2']:.3f}")

        hi_x = max(qh * 1.30, (q_fl or 0) * 1.08)
        xr = np.linspace(min(ql * 0.72, ql - 1), hi_x, 600)
        raw = (np.polyval(par, xr) if f["kind"] == "quadratic"
               else par[0] * np.power(np.clip(xr, 1e-9, None), par[1]) + par[2])
        ax.plot(xr, raw * MM_PER_KM, color=C_FIT, lw=1.7, ls=(0, (5, 3)), alpha=0.85, zorder=4,
                label="same fit, extrapolated (unclipped)")
        ax.axhline(0, color="#444444", lw=0.9, ls=":", zorder=1)
        if s_static is not None:
            ax.axhline(s_static, color=C_IRIS, ls="--", lw=2.2, zorder=5,
                       label="IRIS-SWORD static slope")
        if q_fl:
            ax.axvline(q_fl, color="#e67e22", lw=2.2, ls="-.", zorder=5,
                       label=f"flood driver Q = {q_fl:,.0f} m³/s")

        sig2 = 2 * sigma_S(reach) * MM_PER_KM
        raw_min = float(raw.min() * MM_PER_KM)
        data_lo = min(float(Smm.min()), raw_min)
        med_S = float(np.median(Smm))
        show_zero = (raw_min < 0) or (sig2 > 0.15 * med_S) or (s_static is not None and s_static < 0.25 * med_S)
        if show_zero:
            base = min(0.0, data_lo); lo_mm = base - 0.14 * (Smm.max() - base)
        else:
            lo_mm = data_lo - 0.22 * (Smm.max() - data_lo)
        hi_mm = max(Smm.max(), s_static or 0) + 0.16 * (Smm.max() - lo_mm)
        ax.set_ylim(lo_mm, hi_mm)
        if sig2 > lo_mm:
            ax.axhspan(lo_mm, sig2, color=C_NOISE, alpha=0.22, zorder=1)

        h, l = ax.get_legend_handles_labels()
        h += [Patch(fc=C_SUP, alpha=0.30, ec="none")]
        l += [f"fitted Q support  {ql:,.0f}–{qh:,.0f}"]
        if sig2 > lo_mm:
            h += [Patch(fc=C_NOISE, alpha=0.35, ec="none")]
            l += [f"below 2σ$_S$ = {sig2:.1f} mm/km"]
        else:
            h += [Line2D([], [], ls="none")]
            l += [f"2σ$_S$ = {sig2:.1f} mm/km (off-scale, {sig2/med_S*100:.1f}% of median S)"]

        if f["kind"] == "quadratic":
            qv = shape["vertex_Q"]; sv = np.polyval(par, qv) * MM_PER_KM
            inside = shape["vertex_inside_support"]
            word = "MINIMUM, curve turns back UP" if shape["convex"] else "MAXIMUM, curve peaks then falls"
            if lo_mm < sv < hi_mm and ql * 0.6 < qv < hi_x:
                ax.plot(qv, sv, "o", ms=11, mfc="none", mec="#111111", mew=2.3, zorder=7)
                ax.annotate(f"vertex Q* = {qv:,.0f}\n{word}\n({'inside' if inside else 'outside'} support)",
                            (qv, sv), textcoords="offset points",
                            xytext=(-18, 82) if shape["convex"] else (-96, -74),
                            ha=("right" if shape["convex"] else "center"),
                            fontsize=11.2, fontweight="bold", color="#111111", zorder=9,
                            arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.0),
                            bbox=dict(boxstyle="round,pad=0.30", fc="#fff3cd", ec="#111111", lw=1.3))
            if q_fl and q_fl > qh:
                s_cl = np.polyval(par, qh) * MM_PER_KM
                ax.plot(qh, s_cl, "s", ms=10, mfc="none", mec="#7b241c", mew=2.3, zorder=7)
                ax.annotate(f"_solve_Q clamps here\nS({qh:,.0f}) = {s_cl:.0f} mm/km", (qh, s_cl),
                            textcoords="offset points", xytext=(-120, -66), ha="center",
                            fontsize=11, color="#7b241c", zorder=9,
                            arrowprops=dict(arrowstyle="-|>", color="#7b241c", lw=2.0),
                            bbox=dict(boxstyle="round,pad=0.28", fc="#fdecea", ec="#7b241c", lw=1.3))
            leg_loc, anch = ("lower left", (0.015, 0.15)) if shape["convex"] else ("lower right", None)
        else:
            q0 = shape.get("zero_crossing_Q")
            if q0 and shape.get("zero_inside_support"):
                ax.plot(q0, 0, "o", ms=11, mfc="none", mec="#111111", mew=2.3, zorder=7)
                ax.annotate(f"fit crosses S = 0 at Q = {q0:.0f}\nnp.clip masks the negative slope",
                            (q0, 0), textcoords="offset points", xytext=(86, 66), ha="left",
                            fontsize=11.2, fontweight="bold", color="#111111", zorder=9,
                            arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.0),
                            bbox=dict(boxstyle="round,pad=0.30", fc="#fff3cd", ec="#111111", lw=1.3))
            leg_loc, anch = "upper left", None

        ax.text(0.975, 0.985, sq_equation(f), transform=ax.transAxes, ha="right", va="top",
                fontsize=11.4, color=C_FIT, zorder=9,
                bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=C_FIT, alpha=0.95))
        if s_static is not None:
            ax.text(0.015, s_static, f" {s_static:.1f} mm/km ", transform=ax.get_yaxis_transform(),
                    va="bottom", ha="left", fontsize=11.4, color=C_IRIS, fontweight="bold", zorder=9,
                    bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.80))
        ax.set_xscale("log")
        ax.set_xlabel("on-reach discharge  Q  (m³/s, log)", fontsize=16, fontweight="bold")
        ax.set_ylabel("water-surface slope  S  (mm/km)", fontsize=16, fontweight="bold")
        ax.tick_params(labelsize=13)
        arrow = "↗" if dS > 0 else "↘"
        ax.set_title(f"({LET[col+N]}) S(Q):  S {trend} with Q  {arrow}", fontsize=15.5)
        ax.legend(h, l, loc=leg_loc, bbox_to_anchor=anch, framealpha=0.93, borderpad=0.55)
        ax.grid(alpha=0.3)

        # ---- row 3: stage-discharge --------------------------------------------------
        ax = axs[2, col]
        sd = tw.dropna(subset=["wd", "discharge_cms", "S"])
        sd = sd[(sd.discharge_cms > 0) & (sd.S > 0)]
        sc = ax.scatter(sd.discharge_cms, sd.wd, c=sd.S * MM_PER_KM, s=13, cmap="viridis",
                        alpha=0.85, ec="none", zorder=3,
                        vmin=np.percentile(sd.S * MM_PER_KM, 2),
                        vmax=np.percentile(sd.S * MM_PER_KM, 98))
        cb = fig.colorbar(sc, ax=ax, pad=0.016, fraction=0.038)
        cb.ax.tick_params(labelsize=9.5)   # unit lives in the panel title, so no colorbar label (keeps the column gap clean)
        if q_fl:
            ax.axvline(q_fl, color="#e67e22", lw=2.2, ls="-.", zorder=4)
        ax.set_xscale("log")
        ax.set_xlabel("on-reach discharge  Q  (m³/s, log)", fontsize=16, fontweight="bold")
        ax.set_ylabel("downstream WSE (m)", fontsize=16, fontweight="bold")
        ax.tick_params(labelsize=13)
        ax.set_title(f"({LET[col+2*N]}) stage–discharge at {cfg['gdn']}, coloured by S (mm/km)", fontsize=14.5)
        ax.grid(alpha=0.3)

    # Pull the map row down toward the S(Q) row: uniform hspace left too big a band under row 1,
    # while the row 2 -> row 3 gap must stay (it carries the x-label and the next title). Closing
    # ~60% of the row 1 -> row 2 gap here; the tight bbox on save trims the space this frees at the top.
    for _c in range(N):
        _p0 = axs[0, _c].get_position(); _p1 = axs[1, _c].get_position()
        axs[0, _c].set_position([_p0.x0, _p0.y0 - 0.60 * (_p0.y0 - _p1.y1), _p0.width, _p0.height])

    if suptitle:
        fig.suptitle(suptitle, fontsize=20, fontweight="bold", y=1.004)
    if subtitle:
        fig.text(0.5, 0.9905, subtitle, ha="center", va="top", fontsize=13.4, color="#333333")
    if out_png is not None:
        fig.savefig(out_png, dpi=dpi, bbox_inches="tight", facecolor="white")
    return fig, facts


def sq_onecol_figure(reaches, out_png=None, dpi=300):
    """A single-column figure that reuses the EXACT S(Q) panel design of the main figure's
    row 2 (equation box, fit support, extrapolation, IRIS + flood lines, 2-sigma band,
    vertex/zero annotations, full legend), one panel per reach, stacked for a one-column layout."""
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    n = len(reaches)
    LET = "abcdefgh"
    fig, axs = plt.subplots(n, 1, figsize=(6.7, 5.1 * n), gridspec_kw=dict(hspace=0.30))
    axs = np.atleast_1d(axs)
    for i, reach in enumerate(reaches):
        ax = axs[i]; cfg = ALL_REACHES[reach]
        tw = twin_series(reach); p = sq_pairs(reach, tw=tw)
        Q, S = p.Q_cms.values, p.S.values
        f = fit_sq(Q, S); shape = curve_shape(f); par = f["params"]
        q_fl = cfg.get("q_flood_cms"); s_static = IRIS_STATIC.get(reach)
        trend, dS = reach_trend(reach, f)
        Smm = S * MM_PER_KM
        ax.scatter(Q, Smm, s=15, color=C_PT, alpha=0.26, ec="none", zorder=2,
                   label=f"twin-gauge S vs Q  (n={f['n']:,})")
        ql, qh = f["Q_range"]
        ax.axvspan(ql, qh, color=C_SUP, alpha=0.08, zorder=0)
        xf = np.linspace(ql, qh, 400)
        ax.plot(xf, f["func"](xf) * MM_PER_KM, color=C_FIT, lw=3.0, zorder=5,
                label=f"{f['kind']} fit   R² = {f['r2']:.3f}")
        hi_x = max(qh * 1.30, (q_fl or 0) * 1.08)
        xr = np.linspace(min(ql * 0.72, ql - 1), hi_x, 600)
        raw = (np.polyval(par, xr) if f["kind"] == "quadratic"
               else par[0] * np.power(np.clip(xr, 1e-9, None), par[1]) + par[2])
        ax.plot(xr, raw * MM_PER_KM, color=C_FIT, lw=1.7, ls=(0, (5, 3)), alpha=0.85, zorder=4,
                label="same fit, extrapolated (unclipped)")
        ax.axhline(0, color="#444444", lw=0.9, ls=":", zorder=1)
        if s_static is not None:
            ax.axhline(s_static, color=C_IRIS, ls="--", lw=2.2, zorder=5, label="IRIS-SWORD static slope")
        if q_fl:
            ax.axvline(q_fl, color="#e67e22", lw=2.2, ls="-.", zorder=5,
                       label=f"flood driver Q = {q_fl:,.0f} m³/s")
        sig2 = 2 * sigma_S(reach) * MM_PER_KM
        raw_min = float(raw.min() * MM_PER_KM)
        data_lo = min(float(Smm.min()), raw_min)
        med_S = float(np.median(Smm))
        show_zero = (raw_min < 0) or (sig2 > 0.15 * med_S) or (s_static is not None and s_static < 0.25 * med_S)
        if show_zero:
            base = min(0.0, data_lo); lo_mm = base - 0.14 * (Smm.max() - base)
        else:
            lo_mm = data_lo - 0.22 * (Smm.max() - data_lo)
        hi_mm = max(Smm.max(), s_static or 0) + 0.16 * (Smm.max() - lo_mm)
        ax.set_ylim(lo_mm, hi_mm)
        if sig2 > lo_mm:
            ax.axhspan(lo_mm, sig2, color=C_NOISE, alpha=0.22, zorder=1)
        h, l = ax.get_legend_handles_labels()
        h += [Patch(fc=C_SUP, alpha=0.30, ec="none")]
        l += [f"fitted Q support  {ql:,.0f}–{qh:,.0f}"]
        if sig2 > lo_mm:
            h += [Patch(fc=C_NOISE, alpha=0.35, ec="none")]; l += [f"below 2σ$_S$ = {sig2:.1f} mm/km"]
        else:
            h += [Line2D([], [], ls="none")]
            l += [f"2σ$_S$ = {sig2:.1f} mm/km (off-scale, {sig2/med_S*100:.1f}% of median S)"]
        if f["kind"] == "quadratic":
            qv = shape["vertex_Q"]; sv = np.polyval(par, qv) * MM_PER_KM
            inside = shape["vertex_inside_support"]
            word = "MINIMUM, curve turns back UP" if shape["convex"] else "MAXIMUM, curve peaks then falls"
            if lo_mm < sv < hi_mm and ql * 0.6 < qv < hi_x:
                ax.plot(qv, sv, "o", ms=11, mfc="none", mec="#111111", mew=2.3, zorder=7)
                ax.annotate(f"vertex Q* = {qv:,.0f}\n{word}\n({'inside' if inside else 'outside'} support)",
                            (qv, sv), textcoords="offset points",
                            xytext=(-18, 82) if shape["convex"] else (-96, -74),
                            ha=("right" if shape["convex"] else "center"),
                            fontsize=11.2, fontweight="bold", color="#111111", zorder=9,
                            arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.0),
                            bbox=dict(boxstyle="round,pad=0.30", fc="#fff3cd", ec="#111111", lw=1.3))
            if q_fl and q_fl > qh:
                s_cl = np.polyval(par, qh) * MM_PER_KM
                ax.plot(qh, s_cl, "s", ms=10, mfc="none", mec="#7b241c", mew=2.3, zorder=7)
                ax.annotate(f"_solve_Q clamps here\nS({qh:,.0f}) = {s_cl:.0f} mm/km", (qh, s_cl),
                            textcoords="offset points", xytext=(-120, -66), ha="center",
                            fontsize=11, color="#7b241c", zorder=9,
                            arrowprops=dict(arrowstyle="-|>", color="#7b241c", lw=2.0),
                            bbox=dict(boxstyle="round,pad=0.28", fc="#fdecea", ec="#7b241c", lw=1.3))
            leg_loc, anch = ("lower left", (0.015, 0.15)) if shape["convex"] else ("lower right", None)
        else:
            q0 = shape.get("zero_crossing_Q")
            if q0 and shape.get("zero_inside_support"):
                ax.plot(q0, 0, "o", ms=11, mfc="none", mec="#111111", mew=2.3, zorder=7)
                ax.annotate(f"fit crosses S = 0 at Q = {q0:.0f}\nnp.clip masks the negative slope",
                            (q0, 0), textcoords="offset points", xytext=(86, 66), ha="left",
                            fontsize=11.2, fontweight="bold", color="#111111", zorder=9,
                            arrowprops=dict(arrowstyle="-|>", color="#111111", lw=2.0),
                            bbox=dict(boxstyle="round,pad=0.30", fc="#fff3cd", ec="#111111", lw=1.3))
            leg_loc, anch = "upper left", None
        ax.text(0.975, 0.985, sq_equation(f), transform=ax.transAxes, ha="right", va="top",
                fontsize=11.4, color=C_FIT, zorder=9,
                bbox=dict(boxstyle="round,pad=0.34", fc="white", ec=C_FIT, alpha=0.95))
        if s_static is not None:
            ax.text(0.015, s_static, f" {s_static:.1f} mm/km ", transform=ax.get_yaxis_transform(),
                    va="bottom", ha="left", fontsize=11.4, color=C_IRIS, fontweight="bold", zorder=9,
                    bbox=dict(boxstyle="round,pad=0.14", fc="white", ec="none", alpha=0.80))
        ax.set_xscale("log")
        ax.set_xlabel("on-reach discharge  Q  (m³/s, log)", fontsize=16, fontweight="bold")
        ax.set_ylabel("water-surface slope  S  (mm/km)", fontsize=16, fontweight="bold")
        ax.tick_params(labelsize=13)
        arrow = "↗" if dS > 0 else "↘"
        ax.set_title(f"({LET[i]}) {cfg['river']}:  S {trend} with Q  {arrow}", fontsize=15.5)
        ax.legend(h, l, loc=leg_loc, bbox_to_anchor=anch, framealpha=0.93, borderpad=0.5, fontsize=9)
        ax.grid(alpha=0.3)
    if out_png is not None:
        fig.savefig(out_png, dpi=dpi, bbox_inches="tight", facecolor="white")
    return fig
