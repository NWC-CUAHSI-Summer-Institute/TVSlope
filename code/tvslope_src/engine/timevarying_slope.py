# Time-varying water-surface-slope S(Q) fit + iterative Manning injection.
import numpy as np, pandas as pd
from types import SimpleNamespace
from per_reach3 import twin_series
_SLOPE_COL, _Q_COL, _FEAT = "SLOPE", "discharge_cms", "feature_id"
def sq_pairs(row, mad_k=5.0, min_n=8):
    tw = twin_series(row)
    if tw is None or not len(tw): return None
    d = tw.dropna(subset=["S", "discharge_cms"]).copy()
    d = d[(d.discharge_cms > 0) & (d.S > 0)]
    if len(d) < min_n: return None
    for c in ["S", "discharge_cms"]:
        x = np.log(d[c].values); med = np.median(x); mad = np.median(np.abs(x - med)) or 1e-9
        d = d[np.abs(np.log(d[c].values) - med) <= mad_k * 1.4826 * mad]
    if len(d) < min_n: return None
    return d[["discharge_cms", "S"]].rename(columns={"discharge_cms": "Q_cms"}).reset_index(drop=True)
def _fit_quadratic(Q, S):
    c = np.polyfit(Q, S, 2)
    f = lambda q, c=c: np.clip(np.polyval(c, np.asarray(q, float)), 1e-7, None)
    r2 = 1 - np.sum((S - f(Q))**2) / max(np.sum((S - S.mean())**2), 1e-12)
    lbl = f"S = {c[0]:.2e}Q² {c[1]:+.2e}Q {c[2]:+.2e}"
    return dict(func=f, kind="quadratic", r2=float(r2), params=c.tolist(), label=lbl)
def _fit_powerlaw(Q, S):
    from scipy.optimize import curve_fit
    (a, b, cc), _ = curve_fit(lambda q, a, b, cc: a*np.power(q, b)+cc, Q, S, p0=[np.median(S), 0.3, 0.0], maxfev=10000)
    f = lambda q, a=a, b=b, cc=cc: np.clip(a*np.power(np.asarray(q, float), b)+cc, 1e-7, None)
    r2 = 1 - np.sum((S - f(Q))**2) / max(np.sum((S - S.mean())**2), 1e-12)
    lbl = f"S = {a:.2e}·Q^{b:.2f} {cc:+.2e}"
    return dict(func=f, kind="powerlaw", r2=float(r2), params=[a, b, cc], label=lbl)
def fit_sq(Q, S):
    Q = np.asarray(Q, float); S = np.asarray(S, float); cands = []
    for fn in (_fit_quadratic, _fit_powerlaw):
        try: cands.append(fn(Q, S))
        except Exception: pass
    if not cands: return None
    best = max(cands, key=lambda d: d["r2"]); best["n"] = len(Q)
    best["Q_range"] = (float(np.min(Q)), float(np.max(Q))); best["S_range"] = (float(np.min(S)), float(np.max(S)))
    return best
def _solve_Q(q_orig, s_old, sfunc, q_lo, q_hi, iters=60, tol=1e-4):
    q = float(q_orig)
    for _ in range(iters):
        qc = min(max(q, q_lo), q_hi); s_new = float(sfunc(qc))
        q2 = q_orig * np.sqrt(max(s_new, 1e-9) / max(s_old, 1e-9))
        if abs(q2 - q) <= tol * max(q2, 1.0): q = q2; break
        q = 0.5*(q + q2)
    return q, float(sfunc(min(max(q, q_lo), q_hi)))
def inject_sq(ht, feature_ids, fit):
    ht = ht.copy(); fids = ht[_FEAT].astype("int64"); sfunc = fit["func"]
    q_lo, q_hi = fit["Q_range"]; qcol = ht.columns.get_loc(_Q_COL); scol = ht.columns.get_loc(_SLOPE_COL); changed = 0
    for fid in set(int(f) for f in feature_ids):
        mask = (fids == fid).values
        if not mask.any(): continue
        for i in np.where(mask)[0]:
            q_orig = float(ht.iloc[i, qcol]); s_old = float(ht.iloc[i, scol])
            if not (q_orig > 0 and s_old > 0): continue
            q_new, s_new = _solve_Q(q_orig, s_old, sfunc, q_lo, q_hi)
            ht.iloc[i, qcol] = q_new; ht.iloc[i, scol] = s_new; changed += 1
    return ht, changed
def timevarying_src(row, ht=None, feature_ids=None):
    pairs = sq_pairs(row)
    if pairs is None: return None
    fit = fit_sq(pairs.Q_cms.values, pairs.S.values)
    if fit is None: return None
    out = dict(pairs=pairs, fit=fit)
    if ht is not None and feature_ids is not None:
        ht_new, n = inject_sq(ht, feature_ids, fit); out["ht_new"] = ht_new; out["n_changed"] = n
    return out
def generate_timevarying_fim(*a, **k):
    raise RuntimeError("FIM regeneration is disabled in the standalone notebook, keep REGEN_FIM=False and "
                       "reuse the cached extent tifs (see code/timevarying_slope.py to regenerate).")
TV  = SimpleNamespace(sq_pairs=sq_pairs, fit_sq=fit_sq, _solve_Q=_solve_Q, inject_sq=inject_sq,
                      timevarying_src=timevarying_src, generate_timevarying_fim=generate_timevarying_fim)
