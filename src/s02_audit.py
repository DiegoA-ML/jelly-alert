"""Step 2: go/no-go data audit, before any large download.
Counts unique sighting-days per species in training and test years.
Writes outputs/audit.md and data/interim/species_go.json (species that passed).
A species that fails is dropped from every later step. Nothing is filled in."""
import json, sys
import pandas as pd
from config import RAW, OUT, INTERIM, SPECIES, TRAIN_YEARS, TEST_START, MAX_COORD_UNCERTAINTY_M, MIN_TRAIN, MIN_TEST

def load():
    df = pd.read_csv(RAW / "gbif_occurrences.csv", sep="\t", low_memory=False, on_bad_lines="skip")
    unc = pd.to_numeric(df["coordinateUncertaintyInMeters"], errors="coerce")
    df = df[unc.isna() | (unc <= MAX_COORD_UNCERTAINTY_M)].copy()
    df["date"] = pd.to_datetime(df["eventDate"].astype(str).str[:10], errors="coerce")
    return df.dropna(subset=["date", "decimalLatitude", "decimalLongitude"])

def go_species():
    return json.loads((INTERIM / "species_go.json").read_text())

def main():
    df = load()
    lines = ["# Data audit\n\n", f"Records after quality filter (all taxa): {len(df)}\n"]
    go, summary = [], {}
    for sp in SPECIES:
        s = df[df["species"] == sp].drop_duplicates(["date", "decimalLatitude", "decimalLongitude"])
        tr, te = s[s.date.dt.year.isin(TRAIN_YEARS)], s[s.date >= TEST_START]
        ok = len(tr) >= MIN_TRAIN and len(te) >= MIN_TEST
        go += [sp] if ok else []
        summary[sp] = dict(train=len(tr), test=len(te), go=ok)
        lines += [f"\n## {sp}: train={len(tr)} test={len(te)} -> {'GO' if ok else 'NO-GO'}\n",
                  "\nTop sources (datasetKey):\n```\n", s["datasetKey"].value_counts().head(8).to_string(), "\n```\n",
                  "\nYear x month:\n```\n", pd.crosstab(s.date.dt.year, s.date.dt.month).to_string(), "\n```\n"]
    (OUT / "audit.md").write_text("".join(lines))
    (INTERIM / "species_go.json").write_text(json.dumps(go))
    (INTERIM / "audit_summary.json").write_text(json.dumps(summary, indent=1))
    print("".join(lines))
    if not go:
        sys.exit("NO-GO for every species. Stop: widen region or years in config.py.")

if __name__ == "__main__":
    main()
