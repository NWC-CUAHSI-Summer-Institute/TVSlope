"""Time-varying gauge-slope injection for HAND-FIM SRCs  (work6 · TimeVariantSlopemethod).

The method (adapted from the proposed 'time-variant slope injection' slides, using in-situ gauges instead of
raw SWOT overpasses so we get a dense record):

  Step 1  Pair the TWO-STATION water-surface slope  S(t) = (WSE_up - WSE_dn) / span  with the on-reach USGS
          instantaneous discharge  Q(t)  at matching timestamps  (per_reach3.twin_series).
  Step 2  Quality-check the (S, Q) cloud: drop non-positive/NaN, clip slope/discharge outliers (robust MAD).
  Step 3  Establish a slope-discharge relationship  S(Q)  (non-linear; quadratic S=c0+c1 Q+c2 Q^2 like the
          slides, with a monotone power-law  S=a Q^b + c  fallback), keeping whichever fits better (R^2).
  Step 4  Inject S(Q) into Manning per hydroTable row. The uncalibrated SRC is Q = G(h)*sqrt(S) with the
          geometry term G(h)=Q_orig/sqrt(S_orig) fixed by the terrain, so at each stage we solve the IMPLICIT
             Q = Q_orig * sqrt( S(Q) / S_orig )
          iteratively (seed = Q_orig, the slides' suggested initial guess). Converged Q (and its S=S(Q)) give
          the new, TIME-VARYING stage-discharge pair.
  Step 5  Emit the new SRC; downstream FIMbox / fim_eval treat it like any other injected hydroTable.

Public API:
  sq_pairs(row)                      -> DataFrame(Q_cms, S)         the QC'd (discharge, slope) cloud
  fit_sq(Q, S)                       -> dict(func, kind, r2, ...)   the fitted S(Q) relationship
  inject_sq(ht, feature_ids, fit)    -> (ht_new, n_changed)        iterative-Manning hydroTable rewrite
  timevarying_src(reach, row, ht)    -> dict(fit, src DataFrame)   end-to-end for one reach
"""
import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import sys; from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import per_reach3 as P3

SLOPE_COL, Q_COL, FEAT = "SLOPE", "discharge_cms", "feature_id"


# ---------- Step 1-2 : the (S, Q) cloud, quality-checked ----------
def sq_pairs(row, mad_k=5.0, min_n=8):
    """Daily paired-station slope S(t) vs on-reach discharge Q(t), QC'd. Returns DataFrame(Q_cms, S) or None."""
    tw = P3.twin_series(row)                       # columns: datetime, S (=slope, m/m), discharge_cms, ...
    if tw is None or not len(tw): return None
    d = tw.dropna(subset=["S", "discharge_cms"]).copy()
    d = d[(d.discharge_cms > 0) & (d.S > 0)]       # physical: positive downstream-falling slope + flow
    if len(d) < min_n: return None
    # robust outlier removal (MAD) on log-slope and log-Q — the twin-gauge slope is noisy at low flow
    for c in ["S", "discharge_cms"]:
        x = np.log(d[c].values); med = np.median(x); mad = np.median(np.abs(x - med)) or 1e-9
        d = d[np.abs(np.log(d[c].values) - med) <= mad_k * 1.4826 * mad]
    if len(d) < min_n: return None
    return d[["discharge_cms", "S"]].rename(columns={"discharge_cms": "Q_cms"}).reset_index(drop=True)


# ---------- Step 3 : the S(Q) relationship ----------
def _fit_quadratic(Q, S):
    c = np.polyfit(Q, S, 2)                                        # S = c0 Q^2 + c1 Q + c2  (slides' form)
    f = lambda q, c=c: np.clip(np.polyval(c, np.asarray(q, float)), 1e-7, None)
    r2 = 1 - np.sum((S - f(Q))**2) / max(np.sum((S - S.mean())**2), 1e-12)
    lbl = f"S = {c[0]:.2e}Q² {c[1]:+.2e}Q {c[2]:+.2e}"
    return dict(func=f, kind="quadratic", r2=float(r2), params=c.tolist(), label=lbl)

def _fit_powerlaw(Q, S):
    from scipy.optimize import curve_fit
    (a, b, cc), _ = curve_fit(lambda q, a, b, cc: a*np.power(q, b)+cc, Q, S,
                              p0=[np.median(S), 0.3, 0.0], maxfev=10000)
    f = lambda q, a=a, b=b, cc=cc: np.clip(a*np.power(np.asarray(q, float), b)+cc, 1e-7, None)
    r2 = 1 - np.sum((S - f(Q))**2) / max(np.sum((S - S.mean())**2), 1e-12)
    lbl = f"S = {a:.2e}·Q^{b:.2f} {cc:+.2e}"
    return dict(func=f, kind="powerlaw", r2=float(r2), params=[a, b, cc], label=lbl)

def fit_sq(Q, S):
    """Fit S(Q); keep the better of quadratic (slides) and power-law by R². Q,S are 1-D arrays."""
    Q = np.asarray(Q, float); S = np.asarray(S, float)
    cands = []
    for fn in (_fit_quadratic, _fit_powerlaw):
        try: cands.append(fn(Q, S))
        except Exception: pass
    if not cands: return None
    best = max(cands, key=lambda d: d["r2"]); best["n"] = len(Q)
    best["Q_range"] = (float(np.min(Q)), float(np.max(Q))); best["S_range"] = (float(np.min(S)), float(np.max(S)))
    return best


# ---------- Step 4 : iterative-Manning hydroTable injection ----------
def _solve_Q(q_orig, s_old, sfunc, q_lo, q_hi, iters=60, tol=1e-4):
    """Solve  Q = q_orig * sqrt( S(Q)/s_old )  by fixed-point iteration, S(Q) clamped to the fitted Q-range."""
    q = float(q_orig)
    for _ in range(iters):
        qc = min(max(q, q_lo), q_hi)                       # evaluate S only within the observed Q-support
        s_new = float(sfunc(qc))
        q2 = q_orig * np.sqrt(max(s_new, 1e-9) / max(s_old, 1e-9))
        if abs(q2 - q) <= tol * max(q2, 1.0): q = q2; break
        q = 0.5*(q + q2)                                   # damped update -> robust convergence
    return q, float(sfunc(min(max(q, q_lo), q_hi)))

def inject_sq(ht, feature_ids, fit):
    """Rewrite (discharge_cms, SLOPE) for the given feature_ids using the S(Q) fit + iterative Manning solve.
    Returns (ht_new, n_rows_changed). Rows outside the fit's Q-support use the nearest supported Q (clamped)."""
    ht = ht.copy(); fids = ht[FEAT].astype("int64"); sfunc = fit["func"]
    q_lo, q_hi = fit["Q_range"]; qcol = ht.columns.get_loc(Q_COL); scol = ht.columns.get_loc(SLOPE_COL)
    changed = 0
    for fid in set(int(f) for f in feature_ids):
        mask = (fids == fid).values
        if not mask.any(): continue
        idx = np.where(mask)[0]
        for i in idx:
            q_orig = float(ht.iloc[i, qcol]); s_old = float(ht.iloc[i, scol])
            if not (q_orig > 0 and s_old > 0): continue
            q_new, s_new = _solve_Q(q_orig, s_old, sfunc, q_lo, q_hi)
            ht.iloc[i, qcol] = q_new; ht.iloc[i, scol] = s_new; changed += 1
    return ht, changed


# ---------- Step 5 : end-to-end for one reach (fit + demo SRC) ----------
def timevarying_src(row, ht=None, feature_ids=None):
    """Fit S(Q) for a reach and, if a hydroTable slice is given, return the injected time-varying SRC.
    ht: a hydroTable DataFrame (needs feature_id, stage, discharge_cms, SLOPE); feature_ids: reach's FIM ids."""
    pairs = sq_pairs(row)
    if pairs is None: return None
    fit = fit_sq(pairs.Q_cms.values, pairs.S.values)
    if fit is None: return None
    out = dict(pairs=pairs, fit=fit)
    if ht is not None and feature_ids is not None:
        ht_new, n = inject_sq(ht, feature_ids, fit)
        out["ht_new"] = ht_new; out["n_changed"] = n
    return out


def swap_slope_timevarying(aoi_dir, feature_ids, fit):
    """Like fim_reach.swap_slope but injects the TIME-VARYING S(Q) SRC (iterative Manning) into every branch
    hydroTable for the reach's feature_ids (restores from the one-time .orig baseline so treatments don't
    compound). Returns the number of hydroTables rewritten."""
    import shutil
    wsd = Path(aoi_dir)/"watershed-data"; n = 0
    for ht in sorted((wsd/"branches").glob("*/hydroTable_*.csv")):
        orig = ht.with_name(ht.name + ".orig")
        if not orig.exists(): shutil.copy2(ht, orig)
        base = pd.read_csv(orig)
        base, _ = inject_sq(base, feature_ids, fit)
        base.to_csv(ht, index=False)
        ht.with_suffix(".parquet").unlink(missing_ok=True)      # generateFIM prefers parquet -> drop stale
        n += 1
    return n


def generate_timevarying_fim(row, event_date=None, discharge_cms=None, tag="gauge_timevarying", verbose=True):
    """End-to-end time-varying-slope FIM for one gauge-paired reach: fit S(Q) -> inject into hydroTables ->
    run FIMbox. If discharge_cms is given (e.g. Ohio 2025 gauge flood past the NWM retrospective), the FIM is
    driven by that gauge discharge; otherwise by NWM retrospective at event_date. Returns fim_reach's result dict
    (with extent_tif) or dict(error=...)."""
    import fim_reach as FR
    reach = str(row.reach); huc8 = str(getattr(row, "huc8", getattr(row, "fim_huc8", ""))).zfill(8)
    aoi = FR.stage(huc8)
    if aoi is None: return dict(reach=reach, error="staging failed")
    FR.build_hand_once(aoi)
    fids = FR.reach_feature_ids(aoi, [reach])
    r = timevarying_src(row)
    if r is None: return dict(reach=reach, error="no S(Q)")
    n = swap_slope_timevarying(aoi, fids, r["fit"])
    if verbose: print(f"  [{reach}] injected time-varying S(Q) into {n} hydroTables ({r['fit']['label']}, R²={r['fit']['r2']:.2f})")
    ed = event_date or getattr(row, "bench_date", None) or FR.peak_event_date(str(getattr(row, "gq", "")))
    if discharge_cms is not None:
        ext = _run_fim_from_discharge(aoi, fids, discharge_cms, verbose=verbose)   # gauge-driven (bypasses NWM)
    else:
        ext = FR._run_fim(aoi, ed)                                                 # NWM-driven
    if ext:
        import shutil
        dest = Path(aoi)/"fim-outputs"/f"reach{reach}_{tag}_inundation.tif"; shutil.copy2(ext, dest); ext = dest
    return dict(reach=reach, huc8=huc8, aoi_dir=str(aoi), event_date=ed, feature_ids=sorted(fids),
                fit=r["fit"], extent_tif=(str(ext) if ext else None))


def generate_treatment_fim(row, treatment, slope_mmkm, event_date=None, discharge_cms=None, verbose=True):
    """Gauge-driven FIM for a CONSTANT-slope treatment (baseline/hfirissword/swot_*), for out-of-retrospective
    events (Ohio 2025). Injects the constant slope via fim_reach.swap_slope, then drives FIMbox with the on-reach
    gauge discharge. Writes reach<reach>_<treatment>_gaugedriven.tif. Returns the extent path or None."""
    import fim_reach as FR, shutil
    reach = str(row.reach); huc8 = str(getattr(row, "fim_huc8", getattr(row, "huc8", ""))).zfill(8)
    aoi = FR.stage(huc8)
    if aoi is None: return None
    FR.build_hand_once(aoi)
    fids = FR.reach_feature_ids(aoi, [reach])
    s_new = float(slope_mmkm)/1e6 if (slope_mmkm == slope_mmkm and float(slope_mmkm) > 0) else None
    FR.swap_slope(aoi, {} if (treatment == "baseline" or s_new is None) else {f: s_new for f in fids})
    if verbose: print(f"  [{reach}] {treatment}: S={slope_mmkm:.0f} mm/km, gauge Q={discharge_cms:.0f} m³/s")
    ext = _run_fim_from_discharge(aoi, fids, discharge_cms, verbose=False) if discharge_cms is not None else FR._run_fim(aoi, event_date)
    if ext:
        dest = Path(aoi)/"fim-outputs"/f"reach{reach}_{treatment}_gaugedriven.tif"; shutil.copy2(ext, dest); ext = dest
    return str(ext) if ext else None


def _run_fim_from_discharge(aoi_dir, feature_ids, discharge_cms, verbose=True):
    """Drive FIMbox with the on-reach gauge discharge (m³/s) on the reach's feature_ids, instead of NWM — for
    out-of-retrospective floods where we have the gauge (e.g. Ohio 2025-04-12). Writes a discharge CSV
    (feature_id, discharge_cms) into <AOI>/discharge-inputs/ and generates the FIM from it."""
    import fimbox
    aoi_dir = Path(aoi_dir); ddir = aoi_dir/"discharge-inputs"; ddir.mkdir(parents=True, exist_ok=True)
    fq = ddir/"gauge_flood.csv"
    pd.DataFrame({"feature_id": sorted(int(f) for f in feature_ids),
                  "discharge_cms": float(discharge_cms)}).to_csv(fq, index=False)
    if verbose: print(f"  gauge-driven: {len(feature_ids)} feature_ids @ {discharge_cms:.0f} m³/s -> {fq.name}")
    res = fimbox.generateFIM(aoi_dir, n_workers=_NW, depth=True).from_discharge_inputs(csv=str(fq))
    exts = [Path(getattr(r, "extent_path", "")) for r in (res or []) if getattr(r, "extent_path", None)]
    return exts[-1] if exts else None


_NW = 4


def fig_method(row, aoi_dir, reach, out_png, title=None):
    """Two-panel demo of the time-varying method: (A) the (S,Q) cloud + fitted S(Q); (B) the reach's baseline
    SRC vs the injected time-varying SRC (slope now a function of flow). Returns the fit dict or None."""
    import matplotlib.pyplot as plt, glob
    from pathlib import Path
    pairs = sq_pairs(row)
    if pairs is None: return None
    fit = fit_sq(pairs.Q_cms.values, pairs.S.values)
    if fit is None: return None
    # load the reach's baseline SRC (stage, Q_orig, S_orig) exactly like reach_dossier.src_curve
    hts = glob.glob(str(Path(aoi_dir)/"watershed-data"/"branches"/"*"/"hydroTable_*.csv.orig")) or \
          glob.glob(str(Path(aoi_dir)/"watershed-data"/"branches"/"*"/"hydroTable_*.csv"))
    import fim_reach as FR
    fids = {int(f) for f in FR.reach_feature_ids(aoi_dir, [reach])}
    df = pd.concat([pd.read_csv(h, usecols=["feature_id", "stage", "discharge_cms", "SLOPE"]) for h in hts])
    df = df[df.feature_id.isin(fids)]
    base = df.groupby("stage").discharge_cms.mean().reset_index(); s_base = float(df.SLOPE.median())
    base["stage0"] = base.stage - base.stage.min()
    ql, qh = fit["Q_range"]; qtv, stv = [], []
    for q in base.discharge_cms:
        if q > 0: qn, sn = _solve_Q(float(q), s_base, fit["func"], ql, qh); qtv.append(qn); stv.append(sn*1e6)
        else: qtv.append(np.nan); stv.append(np.nan)
    base["Q_tv"] = qtv; base["S_tv_mmkm"] = stv
    fig, (a, b) = plt.subplots(1, 2, figsize=(15, 6))
    # (A) S(Q) cloud + fit
    a.scatter(pairs.Q_cms, pairs.S*1e6, s=26, color="#8e44ad", alpha=.35, ec="none", label=f"twin-gauge S vs Q (n={fit['n']})")
    xf = np.linspace(ql, qh, 200); a.plot(xf, fit["func"](xf)*1e6, color="#c0392b", lw=3, label=f"{fit['kind']} fit  R²={fit['r2']:.2f}")
    a.axhline(s_base*1e6, color="#0f6fb5", ls="--", lw=2, label=f"static baseline S = {s_base*1e6:.0f} mm/km")
    a.set_xscale("log"); a.set_xlabel("on-reach discharge Q (m³/s, log)"); a.set_ylabel("water-surface slope (mm/km)")
    a.set_title("(A) slope–discharge relationship S(Q)", fontsize=16); a.legend(fontsize=13, loc="best"); a.grid(alpha=.3)
    # (B) baseline vs time-varying SRC
    xmax = float(np.nanpercentile(pairs.Q_cms, 99))
    m = base.discharge_cms <= xmax*1.5
    b.plot(base.discharge_cms[m], base.stage0[m], color="#0f6fb5", lw=3, label=f"static baseline SRC (S={s_base*1e6:.0f} mm/km)")
    b.plot(base.Q_tv[m], base.stage0[m], color="#c0392b", lw=3, label="time-varying SRC  S=S(Q)")
    b.set_xlabel("discharge Q (m³/s)"); b.set_ylabel("stage above low water (m)")
    b.set_title("(B) baseline vs time-varying SRC", fontsize=16); b.legend(fontsize=13, loc="lower right"); b.grid(alpha=.3)
    b.text(.03, .97, f"slope now varies with flow:\n{np.nanmin(stv):.0f}–{np.nanmax(stv):.0f} mm/km", transform=b.transAxes,
           va="top", fontsize=13, bbox=dict(fc="white", ec="0.6", alpha=.9))
    fig.suptitle(title or f"Time-varying gauge-slope injection — {getattr(row,'river','')} {reach}", fontsize=17, y=1.0)
    fig.tight_layout(); fig.savefig(out_png, dpi=145, bbox_inches="tight"); plt.close(fig)
    return fit


if __name__ == "__main__":                                   # quick self-test on the two gauge-paired reaches
    sa = pd.read_csv(Path(__file__).resolve().parent.parent/"output_exp6"/"select"/"study_areas_final.csv",
                     dtype={"reach": str, "gup": str, "gmid": str, "gdn": str, "gq": str})
    for rid in ["74282100101", "75120400053"]:
        row = sa[sa.reach == rid].iloc[0]
        r = timevarying_src(row)
        if r is None: print(f"{rid}: no usable twin-gauge S(Q)"); continue
        f = r["fit"]
        print(f"{rid} {row.river}: n={f['n']} pairs | {f['kind']} fit  {f['label']}  (R²={f['r2']:.2f}) | "
              f"Q {f['Q_range'][0]:.0f}-{f['Q_range'][1]:.0f} m³/s  S {f['S_range'][0]*1e6:.0f}-{f['S_range'][1]*1e6:.0f} mm/km")
