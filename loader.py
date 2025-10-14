# loader.py
import time
import requests
import pandas as pd
import numpy as np

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "assignment_week7/1.0 (your_email@example.com)"

def geocode_location(location, retries=2, pause=1.0):
    params = {"q": location, "format": "json", "limit": 1}
    headers = {"User-Agent": USER_AGENT}
    attempt = 0
    while attempt <= retries:
        try:
            resp = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if not data:
                return None
            r = data[0]
            return {"lat": float(r["lat"]), "lon": float(r["lon"]), "type": r.get("type") or r.get("class")}
        except requests.RequestException:
            attempt += 1
            time.sleep(pause)
    return None

def load_locations(locations, sleep_between=1.0):
    rows = []
    for loc in locations:
        result = None
        try:
            result = geocode_location(loc)
        except Exception:
            result = None
        if result:
            lat, lon, typ = result.get("lat", np.nan), result.get("lon", np.nan), result.get("type", np.nan)
        else:
            lat = lon = typ = np.nan
        rows.append({"Location": loc, "Latitude": lat, "Longitude": lon, "Type": typ})
        time.sleep(sleep_between)
    return pd.DataFrame(rows, columns=["Location", "Latitude", "Longitude", "Type"])
