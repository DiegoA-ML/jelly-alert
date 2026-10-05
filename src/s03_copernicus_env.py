"""Step 3: Copernicus Marine Baltic physics, daily means, surface layer.
For every day from START to END, the first product in CMEMS_PHY_PRODUCTS that has that day is used.
Output: data/raw/cmems_phy_<year>_<rank>.nc and data/raw/env_sources.json (which product covers which days).
Credentials from .env: COPERNICUSMARINE_SERVICE_USERNAME / COPERNICUSMARINE_SERVICE_PASSWORD."""
import json, os, sys
import numpy as np, pandas as pd
import copernicusmarine as cm
from config import RAW, BBOX, START, END, CMEMS_PHY_PRODUCTS, CMEMS_VARS

LOG = RAW / "env_sources.json"

def open_product(dataset_id):
    ds = cm.open_dataset(
        dataset_id=dataset_id, variables=CMEMS_VARS,
        minimum_longitude=BBOX["west"], maximum_longitude=BBOX["east"],
        minimum_latitude=BBOX["south"], maximum_latitude=BBOX["north"],
        minimum_depth=0, maximum_depth=1.5,
        username=os.environ.get("COPERNICUSMARINE_SERVICE_USERNAME"),
        password=os.environ.get("COPERNICUSMARINE_SERVICE_PASSWORD"))
    if "depth" in ds.dims:
        ds = ds.isel(depth=0, drop=True)
    return ds

def main():
    log = json.loads(LOG.read_text()) if LOG.exists() else []
    have = pd.DatetimeIndex(sorted({d for e in log for d in pd.date_range(e["from"], e["to"])
                                    if (RAW / e["file"]).exists()}))
    need = pd.date_range(START, END)
    for rank, (product, dataset_id, label) in enumerate(CMEMS_PHY_PRODUCTS):
        missing = need.difference(have)
        if missing.empty:
            break
        try:
            ds = open_product(dataset_id)
        except Exception as e:
            print(f"skip {dataset_id}: {str(e)[:160]}")
            continue
        days = pd.DatetimeIndex(ds.time.values).floor("D")
        print(f"{dataset_id}: {days.min().date()} to {days.max().date()}")
        for year in sorted(set(missing.year)):
            want = missing[missing.year == year]
            idx = np.where(days.isin(want))[0]
            if idx.size == 0:
                continue
            f = f"cmems_phy_{year}_{rank}.nc"
            sub = ds.isel(time=idx)
            sub = sub.assign_coords(time=days[idx])
            print(f"  downloading {year}: {idx.size} days")
            sub.load().to_netcdf(RAW / f)
            got = days[idx]
            log.append(dict(file=f, product=product, dataset_id=dataset_id, label=label,
                            **{"from": str(got.min().date()), "to": str(got.max().date())}, days=int(idx.size)))
            LOG.write_text(json.dumps(log, indent=1))
            have = have.union(got)
    missing = need.difference(have)
    if len(missing):
        sys.exit(f"{len(missing)} days not available from any product (first {missing[0].date()}, "
                 f"last {missing[-1].date()}). Stopping: gaps are not filled with invented values.")
    print("Ocean data complete.")

if __name__ == "__main__":
    main()
