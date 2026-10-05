"""Run the whole pipeline: uv run --env-file .env python src/run_all.py
Finished steps are skipped (delete data/ or outputs/ to force a rebuild). Stops at the first failure."""
import importlib, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import config
from config import RAW, INTERIM, OUT

STEPS = [
    ("s01_gbif_download",    "Download sightings from GBIF",                  lambda: (RAW / "gbif_citation.txt").exists()),
    ("s02_audit",            "Check there are enough sightings (go/no-go)",   lambda: False),
    ("s03_copernicus_env",   "Download ocean data (Copernicus Marine)",       lambda: False),   # resumes by itself
    ("s04_era5_wind",        "Download wind data (ERA5)",                     lambda: False),   # skips files it has
    ("s05_build_dataset",    "Build grid and training tables",                lambda: False),
    ("s06a_select_features", "Choose features (training years only)",        lambda: False),
    ("s06_train_eval",       "Train and test the model",                      lambda: False),
    ("s07_build_site",       "Build the website into docs/",                  lambda: False),
]

def main():
    for i, (mod, label, done) in enumerate(STEPS, 1):
        print(f"\n=== Step {i}/{len(STEPS)}: {label}")
        if done():
            print("already done")
            continue
        t = time.time()
        importlib.import_module(mod).main()
        importlib.reload(config)    # s06a writes the chosen feature set into config.py
        print(f"--- done in {time.time() - t:.0f} s")
    print("\nFinished. Open docs/index.html. Numbers for the report: outputs/results.md")

if __name__ == "__main__":
    main()
