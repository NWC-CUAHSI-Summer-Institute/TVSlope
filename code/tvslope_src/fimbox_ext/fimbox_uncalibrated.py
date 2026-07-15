# Uncalibrated FIMbox HAND-FIM driver (calibration off, slope injected). Built on FIMbox (github.com/sdmlua/fimbox).
from __future__ import annotations

import argparse
from pathlib import Path

import fimbox
from fimbox import (
    AOIProcessingConfig,
    BranchDerivation,
    calculate_allbranches,
    getAllInputData,
    getNWMretrospective,
    generateFIM,
    run_calibration,
    CalibrationConfig,
)
from fimbox._dask import _resolve_n_workers

FIMBOX_ROOT = Path("/Users/zixun/2026SI/FIMBox_github/fimbox")   # pinned absolute (was relative to code/; kept fixed so this file works from tvslope_src/fimbox_ext/)
DENY_UNIT = FIMBOX_ROOT / "config" / "deny_unit.lst"

def stage_inputs(huc8: str | None, boundary: str | None, out_dir: Path,
                 identifier: str, buffer_m: float) -> Path:
    kw = dict(out_dir=str(out_dir), buffer_m=buffer_m, headwater_buffer_cells=8,
              get_flowlines=True, get_catchments=True, resolution="medium",
              identifier=identifier)
    pp = getAllInputData(huc8=huc8, **kw) if huc8 else getAllInputData(boundary=boundary, **kw)
    pp.run()
    # getAllInputData lays down <out_dir>/<aoi_id>/watershed-data/. Resolve aoi_dir robustly.
    cands = [p.parent for p in out_dir.glob("*/watershed-data") if p.is_dir()]
    aoi_dir = max(cands, key=lambda p: p.stat().st_mtime)        # newest staged AOI
    print(f"[1] staged inputs -> {aoi_dir}")
    return aoi_dir

def build_hand_src(aoi_dir: Path, slope_csv: Path | None) -> None:
    wsd = aoi_dir / "watershed-data"
    ident = next(wsd.glob("*_subset_streams.gpkg")).name.split("_subset_streams")[0]
    BranchDerivation(out_dir=wsd, branch_id_attribute="levpa_id",
                     reach_id_attribute="ID", branch_buffer_distance_meters=7000.0).run()

    def _opt(p: Path):
        return p if p.exists() else None

    cfg = AOIProcessingConfig(
        aoi_dir=wsd,
        branch_list_path=wsd / "branch_ids.lst",
        dem_path=wsd / "dem.tif",
        streams_gpkg=wsd / f"{ident}_subset_streams.gpkg",
        boundary_gpkg=wsd / "wbd_buffered.gpkg",
        bridge_elev_diff_path=_opt(wsd / "bridge_elev_diff.tif"),
        levee_gpkg_path=_opt(wsd / "3d_nld_subset_levees_burned.gpkg"),
        headwaters_gpkg=_opt(wsd / f"{ident}_headwaters.gpkg"),
        levelpaths_extended_gpkg=_opt(wsd / f"{ident}_subset_streams_levelPaths_extended.gpkg"),
        agree_buffer_m=15.0, agree_smooth_drop=10.0, agree_sharp_drop=1000.0,
        cost_distance_tolerance=50.0, lateral_elevation_threshold=10,
        max_split_distance_m=1500.0, slope_min=0.0001, lakes_buffer_dist_m=100.0,
        mannings_n=0.06, stage_min_m=0.0, stage_interval_m=0.3048,
        stage_max_m=25.2984, min_catchment_area=0.25, min_stream_length=0.5,
        crosswalk_max_distance_m=100.0,
        # ---- slope injection (the whole point) ----
        src_slope_source="iris_sword",
        iris_slope_csv=str(slope_csv) if slope_csv else None,   # None -> packaged baseline table
        hfab_slope_column=None,
        n_workers=_resolve_n_workers(), keep_failed_branches=True, delete_deny_list=True,
    )
    result = calculate_allbranches(
        cfg, run_branch_zero=True, delete_deny_list=True,
        deny_unit_list=DENY_UNIT if DENY_UNIT.exists() else None,
        branch_ids_csv=wsd / "branch_ids.csv",
    )
    ok = sum(1 for r in result.branch_results if r.status == "ok")
    print(f"[2] HAND/SRC built (NO calibration): branch_zero=1, non-zero ok={ok}, "
          f"slope_csv={slope_csv or 'PACKAGED-BASELINE'}")

FIMBOX_DATA = FIMBOX_ROOT / "data"
RECURRENCE_FLOWS = FIMBOX_DATA / "nwm3_17C_recurrence_flows_cfs.parquet"       # packaged NWM 3.0 recurrence flows (cfs)
BANKFULL_FLOWS = Path("/Users/zixun/2026SI/slipperyslope/data/fimbox_bankfull_2yr_cms.parquet")   # derived: feature_id, discharge(cms)

def _ensure_bankfull_flows() -> Path:
    if not BANKFULL_FLOWS.exists():
        import pandas as _pd
        _d = _pd.read_parquet(RECURRENCE_FLOWS, columns=["feature_id", "2_0_year_recurrence_flow_17C"])
        _d["discharge"] = _d["2_0_year_recurrence_flow_17C"] * 0.028316846592
        BANKFULL_FLOWS.parent.mkdir(parents=True, exist_ok=True)
        _d[["feature_id", "discharge"]].to_parquet(BANKFULL_FLOWS, index=False)
    return BANKFULL_FLOWS

def apply_subdivision(aoi_dir: Path, channel_n: float, overbank_n: float) -> None:
    wsd = aoi_dir / "watershed-data"
    # SrcSubdiv REQUIRES a vmann_input_file; build a minimal one (defaults fill every feature via default_*_n)
    vmann = wsd / "_vmann_defaults.csv"
    if not vmann.exists():
        import pandas as _pd
        _pd.DataFrame({"feature_id": [0], "channel_n": [channel_n], "overbank_n": [overbank_n]}).to_csv(vmann, index=False)
    cfg = CalibrationConfig(
        src_bankfull_toggle=True, bankfull_flows_file=str(_ensure_bankfull_flows()),   # NWM recurrence bankfull (not observed floods)
        src_subdiv_toggle=True, vmann_input_file=str(vmann),                 # channel/overbank subdivision
        default_channel_n=channel_n, default_overbank_n=overbank_n,
        # every OBSERVATION-fitting routine stays OFF -> not calibrated to the benchmark floods
        src_adjust_usgs=False, src_adjust_ras2fim=False, src_adjust_spatial=False,
        manual_calb_toggle=False, bathymetry_adjust=False,
        nonmonotonic_src_adjustment=False, thalweg_notches_adjustment=False, longitudinal_filter=False,
        aggregate_pre=True, aggregate_post=True, job_branch_limit=_resolve_n_workers(),
    )
    run_calibration(wsd, cfg)
    print("[2b] SRC bankfull + subdivision applied (NO observation calibration); hydroTable keeps "
          "subdiv_discharge_cms/channel_n/overbank_n; discharge_cms is now the subdivided discharge")

def run_streamflow_and_fim(aoi_dir: Path, event: str, n_workers: int,
                           discharge_csv: Path | None = None) -> None:
    if discharge_csv is not None:                       # real-time / observed discharge (out-of-retrospective events)
        print(f"[3] real-time / observed discharge -> {discharge_csv} (NWM retrospective bypassed)")
        results = generateFIM(aoi_dir, n_workers=n_workers, depth=True).from_discharge_inputs(csv=str(discharge_csv))
    else:
        getNWMretrospective(aoi_dir, date=event)
        print(f"[3] NWM retrospective discharge -> {aoi_dir / 'discharge-inputs'}")
        results = generateFIM(aoi_dir, n_workers=n_workers, depth=True).from_discharge_inputs(date=event)
    for r in results:
        print(f"[4] FIM extent -> {r.extent_path}")
    if not results:
        print("[4] no FIM produced — NWM retrospective may not cover this event; supply --discharge-csv "
              "(real-time / observed gauge discharge) for out-of-retrospective floods")

def main() -> None:
    ap = argparse.ArgumentParser(description="Uncalibrated FIMbox FIM driver (slope-injected SRC).")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--huc8")
    g.add_argument("--boundary")
    ap.add_argument("--event", required=True, help='event date/instant, e.g. "2016-01-04"')
    ap.add_argument("--slope-csv", type=Path, default=None,
                    help="feature_id,slope_iris_sword CSV (one per treatment). Omit -> baseline.")
    ap.add_argument("--identifier", default="nwm", help="source-file prefix / treatment tag")
    ap.add_argument("--out-dir", type=Path, default=Path("data/fimbox_out"))
    ap.add_argument("--buffer-m", type=float, default=2000.0)
    ap.add_argument("--skip-stage", action="store_true",
                    help="reuse already-staged inputs + HAND; only (re)build SRC + run FIM")
    ap.add_argument("--no-subdiv", dest="subdiv", action="store_false",
                    help="skip channel/overbank SRC subdivision (drops subdiv_discharge_cms/channel_n/overbank_n); "
                         "subdivision is ON by default so the hydroTable keeps the standard FIM4 columns")
    ap.add_argument("--channel-n", type=float, default=0.06, help="default channel Manning's n for subdivision")
    ap.add_argument("--overbank-n", type=float, default=0.12, help="default overbank Manning's n for subdivision")
    ap.add_argument("--discharge-csv", type=Path, default=None,
                    help="real-time / observed discharge CSV (feature_id, discharge_cms) for events PAST the NWM "
                         "retrospective; bypasses getNWMretrospective")
    args = ap.parse_args()

    print(f"fimbox {getattr(fimbox, '__version__', '?')}  |  calibration: CLOSED  |  "
          f"subdivision: {'ON' if args.subdiv else 'OFF'}  |  "
          f"discharge: {'real-time/observed CSV' if args.discharge_csv else 'NWM retrospective'}")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    n_workers = _resolve_n_workers()

    if args.skip_stage:
        cands = [p.parent for p in args.out_dir.glob("*/watershed-data") if p.is_dir()]
        aoi_dir = max(cands, key=lambda p: p.stat().st_mtime)
    else:
        aoi_dir = stage_inputs(args.huc8, args.boundary, args.out_dir, args.identifier, args.buffer_m)
    build_hand_src(aoi_dir, args.slope_csv)
    if args.subdiv:                                     # keep the standard hydroTable columns; still no observation calibration
        apply_subdivision(aoi_dir, args.channel_n, args.overbank_n)
    run_streamflow_and_fim(aoi_dir, args.event, n_workers, discharge_csv=args.discharge_csv)
    print("done.")

if __name__ == "__main__":
    main()
