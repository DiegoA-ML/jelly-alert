"""Step 4: ERA5 10 m wind (reanalysis-era5-single-levels), 6-hourly.
Credentials from .env: CDSAPI_URL, CDSAPI_KEY. Accept the ERA5 licence once on the dataset page
(https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels, Download tab)."""
import cdsapi, pandas as pd
from config import RAW, BBOX, START, END

_client = None

def request(out, year, months, days):
    global _client
    if out.exists():
        return
    if _client is None:                      # connects on creation, so only when something is missing
        _client = cdsapi.Client()
    _client.retrieve("reanalysis-era5-single-levels", {
        "product_type": ["reanalysis"],
        "variable": ["10m_u_component_of_wind", "10m_v_component_of_wind"],
        "year": [str(year)], "month": [f"{m:02d}" for m in months],
        "day": [f"{d:02d}" for d in days],
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "area": [BBOX["north"] + .25, BBOX["west"] - .25, BBOX["south"] - .25, BBOX["east"] + .25],
        "data_format": "netcdf", "download_format": "unzipped",
    }, str(out))
    print("saved", out.name)

def main():
    end = pd.Timestamp(END)
    for year in range(int(START[:4]), end.year + 1):
        if year < end.year:
            request(RAW / f"era5_wind_{year}.nc", year, range(1, 13), range(1, 32))
        else:   # current year: full months, then the partial last month (avoids asking for future days)
            if end.month > 1:
                request(RAW / f"era5_wind_{year}_a.nc", year, range(1, end.month), range(1, 32))
            request(RAW / f"era5_wind_{year}_b.nc", year, [end.month], range(1, end.day + 1))

if __name__ == "__main__":
    main()
