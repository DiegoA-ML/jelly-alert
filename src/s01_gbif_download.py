"""Step 1: citable GBIF occurrence download (target species + background phyla).
Credentials from .env: GBIF_USER, GBIF_PWD, GBIF_EMAIL (free account at gbif.org).
Output: data/raw/gbif_occurrences.csv + data/raw/gbif_citation.txt (DOI -> cite in report).
Taxon keys are resolved live from the GBIF backbone, never hard-coded."""
import io, os, time, zipfile, requests
from config import RAW, BBOX, START, END, SPECIES, BACKGROUND_PHYLA

API = "https://api.gbif.org/v1"

def taxon_key(name, rank):
    r = requests.get(f"{API}/species/match", params={"name": name, "rank": rank, "strict": "true"}).json()
    if r.get("matchType") in (None, "NONE"):
        raise SystemExit(f"GBIF could not match {name}")
    print(f"  {name}: usageKey={r['usageKey']} ({r['matchType']})")
    return str(r["usageKey"])

def main():
    if (RAW / "gbif_occurrences.csv").exists() and (RAW / "gbif_citation.txt").exists():
        print("GBIF download already present, skipping.")
        return
    for v in ("GBIF_USER", "GBIF_PWD", "GBIF_EMAIL"):
        if not os.environ.get(v):
            raise SystemExit(f"{v} is empty in .env")
    keys = [taxon_key(s, "SPECIES") for s in SPECIES] + [taxon_key(p, "PHYLUM") for p in BACKGROUND_PHYLA]
    b = BBOX
    wkt = (f"POLYGON(({b['west']} {b['south']},{b['east']} {b['south']},{b['east']} {b['north']},"
           f"{b['west']} {b['north']},{b['west']} {b['south']}))")
    body = {
        "creator": os.environ["GBIF_USER"], "notificationAddresses": [os.environ["GBIF_EMAIL"]],
        "sendNotification": False, "format": "SIMPLE_CSV",
        "predicate": {"type": "and", "predicates": [
            {"type": "in", "key": "TAXON_KEY", "values": keys},
            {"type": "equals", "key": "HAS_COORDINATE", "value": "true"},
            {"type": "equals", "key": "HAS_GEOSPATIAL_ISSUE", "value": "false"},
            {"type": "equals", "key": "OCCURRENCE_STATUS", "value": "PRESENT"},
            {"type": "within", "geometry": wkt},
            {"type": "greaterThanOrEquals", "key": "YEAR", "value": START[:4]},
            {"type": "lessThanOrEquals", "key": "YEAR", "value": END[:4]},
        ]},
    }
    auth = (os.environ["GBIF_USER"], os.environ["GBIF_PWD"])
    r = requests.post(f"{API}/occurrence/download/request", json=body, auth=auth)
    r.raise_for_status()
    key = r.text.strip()
    print("download key:", key)
    while True:
        meta = requests.get(f"{API}/occurrence/download/{key}").json()
        print("  status:", meta["status"])
        if meta["status"] == "SUCCEEDED":
            break
        if meta["status"] in ("FAILED", "KILLED", "CANCELLED"):
            raise SystemExit(meta)
        time.sleep(30)
    z = zipfile.ZipFile(io.BytesIO(requests.get(meta["downloadLink"]).content))
    csv_name = [n for n in z.namelist() if n.endswith(".csv")][0]
    (RAW / "gbif_occurrences.csv").write_bytes(z.read(csv_name))
    (RAW / "gbif_citation.txt").write_text(
        f"GBIF.org ({time.strftime('%d %B %Y')}) GBIF Occurrence Download https://doi.org/{meta['doi']}\n"
        f"records: {meta.get('totalRecords')}\nkeys: {keys}\n")
    print("saved; cite:", meta["doi"])

if __name__ == "__main__":
    main()
