"""Portable path resolution for the FIMbox drivers.

These drivers are launched as standalone scripts (subprocess, or `python -m`), so they cannot import
`final_config`. This mirrors its resolver so nothing in the repository carries an absolute path to one
machine.

Resolution order:
  data root   $SLOPE_ROOT, else the nearest parent holding `.slope_root` or a `data/` directory
  FIMbox      $FIMBOX_ROOT, else the installed `fimbox` package's own location
"""
import os
from pathlib import Path

__all__ = ["ROOT", "DATA", "SWORD", "FB", "fimbox_root", "fimbox_src", "fimbox_config",
           "slope_treatments_csv", "bankfull_flows"]


def _repo_root() -> Path:
    env = os.environ.get("SLOPE_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    here = Path(__file__).resolve()
    for cand in here.parents:
        if (cand/".slope_root").exists() or (cand/"data").is_dir():
            return cand
    return here.parents[2]


ROOT = _repo_root()
DATA = ROOT/"data"
SWORD = DATA/"SWORD_v17b_gpkg"/"na_sword_reaches_v17b.gpkg"
FB = DATA/"fimbox_out"


def fimbox_root() -> Path | None:
    """The FIMbox checkout, for its config files. $FIMBOX_ROOT, else the installed package."""
    env = os.environ.get("FIMBOX_ROOT")
    if env:
        return Path(env).expanduser().resolve()
    try:
        import fimbox
        p = Path(fimbox.__file__).resolve()
        # There can be two `config` dirs (src/fimbox/config and the checkout's own). The deny lists
        # live in the checkout's, so probe for one rather than taking the first `config` seen.
        for cand in p.parents:
            if (cand/"config"/"deny_unit.lst").exists():
                return cand
        for cand in p.parents:
            if (cand/"config").is_dir():
                return cand
        return p.parents[1]
    except Exception:
        return None


def fimbox_src() -> Path | None:
    """The directory to put on sys.path so `import fimbox` works from a source checkout."""
    r = fimbox_root()
    if r is None:
        return None
    return r/"src" if (r/"src").is_dir() else r


def fimbox_config(name: str) -> Path | None:
    """A FIMbox config file (deny_unit.lst, deny_branch_zero.lst), or None if FIMbox is not resolvable."""
    r = fimbox_root()
    if r is None:
        return None
    p = r/"config"/name
    return p if p.exists() else None


def slope_treatments_csv() -> Path:
    """The slope-treatment table: the committed copy first, then the staged tree's."""
    for c in (DATA/"slope_treatments.csv", ROOT/"output_exp6"/"select"/"slope_treatments.csv"):
        if c.exists():
            return c
    raise FileNotFoundError(f"slope_treatments.csv not found under {DATA} -- set $SLOPE_ROOT")


def bankfull_flows() -> Path:
    """The 2-year recurrence (bankfull) discharge table, committed in data/."""
    p = DATA/"fimbox_bankfull_2yr_cms.parquet"
    if p.exists():
        return p
    raise FileNotFoundError(f"{p} not found -- set $SLOPE_ROOT to the repository root")
