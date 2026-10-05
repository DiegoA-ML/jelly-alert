"""Step 5: put all ocean and wind data on one ~5.5 km grid, then build training tables.
Presence   = a (cell, day) with a sighting of the species.
Background = a (cell, day) with a sighting of any target-group animal (observer-effort correction).
For lead L, the features come from day t-L: "what did the ocean look like L days before the sighting"."""
import glob, re
import numpy as np, pandas as pd, xarray as xr
from scipy.spatial import cKDTree
from config import (RAW, INTERIM, LEAD_DAYS, SNAP_MAX_KM, FEATURES, AT_SEA_MIN_KM,
                    BBOX, GRID_DLAT, GRID_DLON)
from s02_audit import load, go_species

KM_LAT, KM_LON = 110.57, np.cos(np.deg2rad(56.1)) * 111.32

def _std(ds):
    ren = {k: v for k, v in {"latitude": "lat", "longitude": "lon", "valid_time": "time"}.items()
           if k in ds.dims or k in ds.coords}
    ds = ds.rename(ren)
    if "depth" in ds.dims:
        ds = ds.isel(depth=0, drop=True)
    drop = [v for v in ("number", "expver", "depth") if v in ds.coords]
    return ds.drop_vars(drop).sortby("lat").sortby("lon")

def grid():
    lat = np.round(np.arange(BBOX["south"] + GRID_DLAT / 2, BBOX["north"], GRID_DLAT), 4)
    lon = np.round(np.arange(BBOX["west"] + GRID_DLON / 2, BBOX["east"], GRID_DLON), 4)
    return lat, lon

def _regrid(ds, lat, lon):
    """Block-average the native grid to ~target size, then take the nearest block per target cell.
    Different products have different native grids; this puts them all on the same one."""
    ky = max(1, round(GRID_DLAT / float(abs(ds.lat[1] - ds.lat[0]))))
    kx = max(1, round(GRID_DLON / float(abs(ds.lon[1] - ds.lon[0]))))
    if ky > 1 or kx > 1:
        ds = ds.coarsen(lat=ky, lon=kx, boundary="trim").mean()
    return ds.interp(lat=lat, lon=lon, method="nearest")

def _dedup(ds):
    return ds.isel(time=~ds.get_index("time").duplicated())

def build_env():
    lat, lon = grid()
    files = sorted(glob.glob(str(RAW / "cmems_phy_*.nc")),
                   key=lambda f: tuple(map(int, re.findall(r"_(\d+)_(\d+)\.nc$", f)[0][::-1])))  # rank, year
    parts = []
    for f in files:
        ds = _std(xr.open_dataset(f))[["thetao", "so", "uo", "vo"]].astype("float32")
        ds["time"] = ds.time.dt.floor("D")
        parts.append(_regrid(ds.load(), lat, lon))
        print("regridded", f.split("/")[-1])
    phy = _dedup(xr.concat(parts, "time")).sortby("time")      # lower rank wins on overlap
    winds = []
    for f in sorted(glob.glob(str(RAW / "era5_wind_*.nc"))):
        w = _std(xr.open_dataset(f))[["u10", "v10"]].astype("float32")
        winds.append(w.resample(time="1D").mean().load())
    wind = _dedup(xr.concat(winds, "time").sortby("time"))
    wind = wind.reindex(time=phy.time).interp(lat=lat, lon=lon)
    env = xr.Dataset({"sst": phy.thetao, "sss": phy.so, "cur": np.hypot(phy.uo, phy.vo),
                      "u10": wind.u10, "v10": wind.v10})
    env["sst_trend7"] = env.sst - env.sst.shift(time=7)
    sea = (env.sst.notnull().mean("time") > 0.99)                # a cell is sea if valid on >99% of days
    env = env[FEATURES].where(sea)
    env["sea"] = sea
    env.to_netcdf(INTERIM / "env.nc")
    return env

def open_env():
    p = INTERIM / "env.nc"
    return xr.open_dataset(p).load() if p.exists() else build_env()

def cell_xy(env, mask):
    LAT, LON = np.meshgrid(env.lat.values, env.lon.values, indexing="ij")
    iy, ix = np.where(mask)
    return iy, ix, np.c_[LAT[iy, ix] * KM_LAT, LON[iy, ix] * KM_LON]

def coast_km(env):
    """Distance (km) from every sea cell to the nearest land cell, in sea-cell order."""
    sea = env.sea.values.astype(bool)
    iy, ix, sea_xy = cell_xy(env, sea)
    _, _, land_xy = cell_xy(env, ~sea)
    return iy, ix, cKDTree(land_xy).query(sea_xy)[0]

def snap(df, env):
    """Snap each sighting to its nearest sea cell; tag open water (>= AT_SEA_MIN_KM from land)."""
    sea = env.sea.values.astype(bool)
    iy, ix, sea_xy = cell_xy(env, sea)
    _, _, land_xy = cell_xy(env, ~sea)
    pts = np.c_[df.decimalLatitude * KM_LAT, df.decimalLongitude * KM_LON]
    d, i = cKDTree(sea_xy).query(pts)
    dl, _ = cKDTree(land_xy).query(pts)
    df = df.assign(iy=iy[i], ix=ix[i], dist_km=d, coast_km=dl, at_sea=dl >= AT_SEA_MIN_KM)
    return df[df.dist_km <= SNAP_MAX_KM]

def features(cells, env, lead):
    t = cells.date - pd.Timedelta(days=lead)
    ok = (t >= pd.Timestamp(env.time.values[0])) & (t <= pd.Timestamp(env.time.values[-1]))
    cells, t = cells[ok], t[ok]
    ti = pd.Index(env.time.values).get_indexer(t)
    X = {f: env[f].values[ti, cells.iy.values, cells.ix.values] for f in FEATURES}
    return pd.concat([cells.reset_index(drop=True), pd.DataFrame(X)], axis=1).dropna(subset=FEATURES)

def main():
    env = open_env()
    occ = snap(load(), env)
    bg = occ.drop_duplicates(["iy", "ix", "date"])[["iy", "ix", "date", "at_sea"]]
    for sp in go_species():
        tag = sp.replace(" ", "_")
        pr = occ[occ.species == sp].drop_duplicates(["iy", "ix", "date"])
        pr[["iy", "ix", "date", "at_sea", "decimalLatitude", "decimalLongitude"]].to_csv(INTERIM / f"obs_{tag}.csv", index=False)
        for L in LEAD_DAYS:
            tab = pd.concat([features(pr[["iy", "ix", "date", "at_sea"]], env, L).assign(y=1),
                             features(bg, env, L).assign(y=0)])
            tab.to_csv(INTERIM / f"train_{tag}_L{L}.csv", index=False)
            print(f"{sp} L={L}: presence={int(tab.y.sum())} (open water {int(tab[tab.at_sea].y.sum())}), "
                  f"background={int((tab.y == 0).sum())}")

if __name__ == "__main__":
    main()
