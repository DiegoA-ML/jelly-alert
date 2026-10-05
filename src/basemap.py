"""Land outline and place names for the website map, so it needs no tile server or API key.
Source: Natural Earth 1:10m land, minor islands and populated places (public domain, naturalearthdata.com).
Clipped to the map region and simplified; cached in data/interim/basemap.json."""
import json
import requests
from shapely.geometry import box, shape, mapping
from shapely.ops import unary_union
from config import RAW, INTERIM, BBOX

NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
LAYERS = ["ne_10m_land", "ne_10m_minor_islands", "ne_10m_populated_places_simple"]
OUT = INTERIM / "basemap.json"
PAD = 6.0          # degrees around BBOX, so the land never stops inside the view
MAX_RANK = 8       # Natural Earth scalerank: lower = bigger place; keeps the map uncluttered

def fetch(name):
    p = RAW / f"{name}.geojson"
    if not p.exists():
        r = requests.get(NE + f"{name}.geojson", timeout=120)
        r.raise_for_status()
        p.write_bytes(r.content)
    return json.loads(p.read_text())

def build():
    clip = box(BBOX["west"] - PAD, BBOX["south"] - PAD, BBOX["east"] + PAD, BBOX["north"] + PAD)
    land, islands, places = (fetch(n) for n in LAYERS)
    geoms = [shape(f["geometry"]).intersection(clip) for f in land["features"] + islands["features"]]
    poly = unary_union([g for g in geoms if not g.is_empty]).simplify(0.003, preserve_topology=True)
    inner = box(BBOX["west"], BBOX["south"], BBOX["east"], BBOX["north"])
    names = sorted(([f["properties"]["name"], round(f["geometry"]["coordinates"][1], 3),
                     round(f["geometry"]["coordinates"][0], 3), f["properties"]["scalerank"]]
                    for f in places["features"]
                    if f["properties"]["scalerank"] <= MAX_RANK and inner.contains(shape(f["geometry"]))),
                   key=lambda x: x[3])
    def rnd(c):
        return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 3), round(c[1], 3)]
    g = mapping(poly)
    out = dict(land=dict(type=g["type"], coordinates=rnd(g["coordinates"])), places=names)
    OUT.write_text(json.dumps(out, separators=(",", ":")))
    return out

def load():
    return json.loads(OUT.read_text()) if OUT.exists() else build()

if __name__ == "__main__":
    b = build()
    print(f"basemap: {len(json.dumps(b)) // 1024} KB, {len(b['places'])} places:", [p[0] for p in b["places"]])
