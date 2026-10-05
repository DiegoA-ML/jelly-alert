"""Single source of truth for scope. Change settings here, nowhere else."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW, INTERIM, OUT, DOCS = ROOT / "data/raw", ROOT / "data/interim", ROOT / "outputs", ROOT / "docs"
for p in (RAW, INTERIM, OUT, DOCS):
    p.mkdir(parents=True, exist_ok=True)

# Region: Danish inner waters (Kattegat, Belt Sea, Øresund, western Baltic)
BBOX = dict(west=9.0, east=13.1, south=54.5, north=57.8)

# Time split. Training years are never shown on the map (that would be in-sample).
START, END = "2015-01-01", "2026-09-15"
TRAIN_YEARS = list(range(2015, 2025))    # 2015-2024
TEST_YEARS = [2025, 2026]                # held out, never seen in training
TEST_START = "2025-01-01"
MAP_SEASON = ("05-01", "09-15")          # map shows 1 May - 15 September of each test year

SPECIES = ["Cyanea capillata", "Aurelia aurita"]
COMMON = {"Cyanea capillata": "Lion's mane", "Aurelia aurita": "Moon jelly"}
DANISH = {"Cyanea capillata": "brandmand", "Aurelia aurita": "vandmand"}
# Target-group background: other animals reported by the same people and methods,
# so the model learns "jellyfish vs. other sea life", not "where people look".
BACKGROUND_PHYLA = ["Cnidaria", "Ctenophora", "Echinodermata"]

LEAD_DAYS = [0, 1, 3, 5, 7, 10]
MAP_LEAD = 5
GRID_DLAT, GRID_DLON = 0.05, 0.0833      # common ~5.5 km grid for every year and product
SNAP_MAX_KM = 5.0                         # sightings further than this from a sea cell are dropped
MAX_COORD_UNCERTAINTY_M = 5000

# Open water vs. shore. Cells/sightings >= AT_SEA_MIN_KM from land count as open water.
AT_SEA_MIN_KM = 5.0
MIN_AT_SEA_TRAIN = 150    # train on open-water sightings only if at least this many exist
MIN_AT_SEA_TEST = 20      # report a separate open-water score only if at least this many exist

# Audit thresholds (unique sighting-days); below these a species is dropped, not faked.
MIN_TRAIN, MIN_TEST = 150, 25

# Copernicus Marine Baltic physics, daily means, surface layer. For each day, products are
# tried in this order and the one used is logged in data/raw/env_sources.json (shown on the site).
# IDs that do not exist are skipped. Check with: uv run copernicusmarine describe -i <dataset_id>
CMEMS_PHY_PRODUCTS = [
    ("BALTICSEA_MULTIYEAR_PHY_003_011", "cmems_mod_bal_phy_my_P1D-m", "Reanalysis"),
    ("BALTICSEA_MULTIYEAR_PHY_003_011", "cmems_mod_bal_phy_myint_P1D-m", "Reanalysis, interim"),
    ("BALTICSEA_ANALYSISFORECAST_PHY_003_006", "cmems_mod_bal_phy_anfc_P1D-m", "Operational analysis"),
]
CMEMS_VARS = ["thetao", "so", "uo", "vo"]

# Provisional feature set: physics + wind, identical for every year.
FEATURES = ["sst", "sss", "cur", "u10", "v10", "sst_trend7"]
FEATURE_LABELS = {
    "sst": "Sea surface temperature",
    "sss": "Surface salinity",
    "cur": "Surface current speed",
    "u10": "Wind, west-east component",
    "v10": "Wind, south-north component",
    "sst_trend7": "Temperature change over the previous 7 days",
}
