# Jelly Alert: prototype

Can public ocean and wind data tell us where jellyfish will be a few days ahead?
This prototype tests that for lion's mane (*Cyanea capillata*, brandmand) and moon jelly (*Aurelia aurita*, vandmand)
in Danish inner waters, and shows the result as a website: a map that replays the held-out 2025 and 2026 seasons
next to the real sightings.

DTU course 25352 Blue Bioeconomy Innovation. Study prototype, not a product.

## Order of work

1. Create the three free accounts below.
2. Open this folder in VS Code, start Claude Code (Opus, medium effort) and paste `CLAUDE_CODE_PROMPT.md`. It creates `.env` and tells you when to paste your credentials into it. Then it runs everything and publishes the website.
3. Make the pitch deck: follow `PITCH_PROMPT.md` in a claude.ai chat inside the 25352_BBI project (Opus, high effort).
4. Fill in and send `TEAM_MESSAGE.md` to the team.

## What you need (once)

Three free accounts. Put the credentials in `.env` (copy `.env.example`). `.env` is never committed.

| # | Account | What it gives | Link |
|---|---|---|---|
| 1 | GBIF | Jellyfish and other sea-life sightings, with a citable DOI | https://www.gbif.org (Register) |
| 2 | Copernicus Marine | Baltic Sea temperature, salinity, currents (daily) | https://data.marine.copernicus.eu/register |
| 3 | Copernicus Climate Data Store | ERA5 wind | https://cds.climate.copernicus.eu (Register, API token on your profile page) |

For account 3 you must also accept the ERA5 licence once: open
https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels, Download tab, accept.

## Run

Requires only [uv](https://docs.astral.sh/uv/). Nothing is installed outside the project.

```bash
uv sync
uv run --env-file .env python src/run_all.py
open docs/index.html
```

Downloads take 1 to 3 hours the first time (the GBIF queue and the Copernicus downloads are the slow parts).
Finished steps are skipped on a rerun, so an interrupted run can simply be started again.

## What the pipeline does

| Step | Script | Output |
|---|---|---|
| 1 | `s01_gbif_download.py` | Sightings in the region 2015 to 2026 (`data/raw/`, DOI in `gbif_citation.txt`) |
| 2 | `s02_audit.py` | Go/no-go per species: enough sightings to train and test? (`outputs/audit.md`) |
| 3 | `s03_copernicus_env.py` | Daily ocean data. Uses the reanalysis where it exists, the operational product after that. Logs which product covers which days |
| 4 | `s04_era5_wind.py` | Daily wind |
| 5 | `s05_build_dataset.py` | Everything on one ~5.5 km grid; training tables for 0, 1, 3, 5, 7, 10 days ahead |
| 6a | `s06a_select_features.py` | Picks the input set by leave-one-year-out cross-validation on 2015 to 2024 only (`outputs/feature_selection.md`) |
| 6 | `s06_train_eval.py` | MaxEnt model per species and lead time; scored once on 2025 to 2026 vs. a calendar-only baseline (`outputs/skill.json`, charts) |
| 7 | `s07_build_site.py` | Website in `docs/` and the report numbers in `outputs/results.md`. Land outline from Natural Earth (`basemap.py`), so the map needs no tile server or API key |

All settings live in `src/config.py`.

## Rules the code follows

- Train 2015 to 2024, test 2025 to 2026. The map only shows test years.
- Every map day uses only data from 5 days earlier.
- No invented data. Missing days stop the run; species without enough sightings are dropped, not padded.

## Related work: GoJelly

The GoJelly Risk Map (EU project GoJelly, 2018 to 2021) forecasts moon jelly blooms in the Baltic by simulating
the life cycle and drifting the jellyfish with an ocean model. Jelly Alert differs in four ways:

1. It does not need to know where polyp beds are (the seabed patches where young jellyfish start life), which are mostly unknown; it learns from where adult jellyfish were seen.
2. It is tested against real sightings from years it never saw. The GoJelly authors state their framework has not yet been formally validated for lack of data.
3. It predicts specific dates 0 to 10 days ahead from that day's real ocean conditions, not monthly scenarios from one simulated year (2021).
4. It covers lion's mane as well as moon jelly, and collects new sightings from users.

GoJelly is stronger at explaining why blooms form and at what-if scenarios. No GoJelly code or data is used here.

- Cant, J. et al. (2025) Coupling hydrodynamic drifting simulations and seasonal demographics to unmask the drivers of jellyfish blooms. *Journal of Applied Ecology*. https://doi.org/10.1111/1365-2664.70186
- Code: https://github.com/CantJ/Bloom-forecasting-tools, archived at https://doi.org/10.5281/zenodo.17154611 (CC BY 4.0)

## Website

`docs/` is the website (GitHub Pages: Settings, Pages, branch `main`, folder `/docs`).
`index.html` is the map; `about.html` explains the method, the data sources and the limits.
