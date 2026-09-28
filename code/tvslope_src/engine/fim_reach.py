# Reach -> NWM feature_id resolution (RiverJoin-style) + AOI directory lookup.
from pathlib import Path
from types import SimpleNamespace
import geopandas as gpd, pyogrio
from final_config import DATA, SWORD
FIMBOX_OUT = DATA/"fimbox_out"; FIMBOX_OUT.mkdir(parents=True, exist_ok=True)
def _aoi_dir(huc8):
    huc8 = str(huc8).zfill(8)
    for c in [FIMBOX_OUT/f"HUC{huc8}"] + [p.parent for p in FIMBOX_OUT.glob(f"*{huc8}*/watershed-data")]:
        if (c/"watershed-data").is_dir(): return c
    return None
def reach_feature_ids(aoi_dir, reach_ids, tol_m=1000.0):
    if isinstance(reach_ids, (str, int)): reach_ids = [reach_ids]
    streams = Path(aoi_dir)/"watershed-data"/"baseline_subset_streams.gpkg"
    if not streams.exists():
        streams = next((Path(aoi_dir)/"watershed-data").glob("*_subset_streams.gpkg"), None)
    if streams is None: return set()
    nwm = pyogrio.read_dataframe(streams, columns=["ID"]).to_crs(5070)
    lines = []
    for r in reach_ids:
        try:
            gg = pyogrio.read_dataframe(SWORD, where=f"reach_id = {int(r)}")
            if len(gg): lines.append(gg.set_crs(4326, allow_override=True).to_crs(5070).geometry.iloc[0])
        except Exception: pass
    if not lines: return set()
    rl = gpd.GeoDataFrame(geometry=lines, crs=5070)
    j = gpd.sjoin_nearest(nwm, rl, distance_col="d", max_distance=tol_m)
    return set(j.ID.astype("int64").tolist())
FR  = SimpleNamespace(SWORD=SWORD, FIMBOX_OUT=FIMBOX_OUT, _aoi_dir=_aoi_dir, reach_feature_ids=reach_feature_ids)
