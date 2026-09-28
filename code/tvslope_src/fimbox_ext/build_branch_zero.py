# Build + prune branch-0 HAND/hydroTable to a tributary gap-filler. Built on FIMbox (github.com/sdmlua/fimbox).
import os, sys, time, glob, warnings
warnings.filterwarnings("ignore")
os.environ.pop("PROJ_DATA", None); os.environ.pop("PROJ_LIB", None)
os.environ.setdefault("MPLBACKEND", "Agg")
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fimbox.preprocessing.calculate_branch.process_branches import (
    AOIProcessingConfig, _resolve_paths, _process_single_branch)

ROOT = Path("/Users/zixun/2026SI/slipperyslope"); FB = ROOT/"data/fimbox_out"
HUCS = os.environ.get("BRANCH0_HUCS", "05140101,07130011,07140105,10170203,10230003").split(",")
FORCE = bool(os.environ.get("FORCE_BRANCH0"))
DENY = Path("/Users/zixun/2026SI/FIMBox_github/fimbox/config/deny_branch_zero.lst")   # FIMbox's own branch-0 cleanup list

def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)

def branch_zero_built(wsd):
    b0 = Path(wsd)/"branches"/"0"
    return (b0/"rem_zeroed_masked_0.tif").exists() and (b0/"hydroTable_0.csv").exists()

def gapfill_prune(wsd):
    import pandas as _pd
    wsd = Path(wsd); b0 = wsd/"branches"/"0"
    lp = set()
    for h in glob.glob(str(wsd/"branches/*/hydroTable_*.csv")):
        if Path(h).parent.name == "0": continue                      # skip branch 0 itself
        lp |= set(_pd.read_csv(h, usecols=["feature_id"]).feature_id.astype("int64"))
    kept = 0
    for name in ("hydroTable_0.csv", "src_full_crosswalked_0.csv"):
        f = b0/name
        if not f.exists(): continue
        df = _pd.read_csv(f)
        df = df[~df.feature_id.astype("int64").isin(lp)]             # keep only branch-0-only (tributary) fids
        df.to_csv(f, index=False)
        kept = df.feature_id.nunique()
    return kept

def cleanup_branch_zero(b0):
    b0 = Path(b0)
    if not DENY.exists(): return 0
    freed = 0
    for ln in DENY.read_text().splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"): continue          # commented => KEEP (allow-list)
        p = b0 / ln.replace("{}", "0")
        if p.is_file() or p.is_symlink():
            freed += p.stat().st_size if p.is_file() else 0; p.unlink()
    dem0 = b0/"dem_0.tif"                                    # restore the whole-AOI DEM link downstream tools expect
    if not dem0.exists():
        try: dem0.symlink_to(Path("../../dem.tif"))
        except Exception: pass
    return freed

def build_branch_zero(wsd, force=False):
    wsd = Path(wsd); huc = wsd.parent.name
    if branch_zero_built(wsd) and not force:
        log(f"  {huc}: branch 0 already built -> skip"); return False
    b0 = wsd/"branches"/"0"; b0.mkdir(parents=True, exist_ok=True)
    dem0 = b0/"dem_0.tif"                         # BranchZero does shutil.copy2(dem.tif, dem_0.tif);
    if dem0.is_symlink() or dem0.exists(): dem0.unlink()   # the pre-seeded symlink -> SameFileError, so drop it
    cfg = AOIProcessingConfig(aoi_dir=wsd, n_workers=1, delete_deny_list=False, keep_failed_branches=True)
    cfg = _resolve_paths(cfg)                     # suffix-glob resolves streams/catchments/headwaters (prefix-robust); boundary=wbd8_clp
    log(f"  {huc}: building branch 0 (BranchZero + CreateHAND, whole-AOI)... "
        f"streams={Path(cfg.streams_gpkg).name} boundary={Path(cfg.boundary_gpkg).name}")
    t0 = time.time(); res = _process_single_branch(cfg, "0")
    if res.status != "ok":
        raise RuntimeError(f"{huc}: branch-0 build FAILED status={res.status} error={getattr(res,'error','')!r}")
    if not branch_zero_built(wsd):
        raise RuntimeError(f"{huc}: branch-0 build reported ok but rem_zeroed_masked_0.tif / hydroTable_0.csv missing")
    log(f"  {huc}: branch 0 built OK in {time.time()-t0:.0f}s -> {b0/'hydroTable_0.csv'}")
    kept = gapfill_prune(wsd)                      # gap-filler: keep only tributary fids (drop mainstem-overlap)
    log(f"  {huc}: gap-filler prune -> branch 0 now {kept} tributary-only feature_ids")
    freed = cleanup_branch_zero(b0)               # trim intermediates (match level-path branches; reclaim disk)
    log(f"  {huc}: cleaned branch-0 intermediates (~{freed/1e9:.2f} GB reclaimed)")
    (wsd/"_subdiv.done").unlink(missing_ok=True)  # force regen_subdiv to re-subdivide INCLUDING branch 0
    for o in glob.glob(str(wsd/"branches/*/hydroTable_*.csv.orig")): Path(o).unlink()
    log(f"  {huc}: invalidated _subdiv.done + .orig (regen_subdiv_fim.py will re-subdivide incl branch 0)")
    return True

def main():
    log(f"build_branch_zero | HUCs={HUCS} | FORCE={FORCE}")
    built = 0
    for huc in HUCS:
        wsd = FB/f"HUC{huc.strip()}"/"watershed-data"
        if not wsd.is_dir(): log(f"  HUC{huc}: no watershed-data dir -> skip"); continue
        try:
            if build_branch_zero(wsd, force=FORCE): built += 1
        except Exception as e:
            import traceback
            log(f"  HUC{huc}: ERROR {e}\n{traceback.format_exc()[-800:]}"); raise
    log(f"BUILD BRANCH ZERO DONE ({built} built, {len(HUCS)-built} skipped/absent)")

if __name__ == "__main__":
    main()
