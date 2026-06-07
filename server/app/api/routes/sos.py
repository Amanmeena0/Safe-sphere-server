import os
import json
from fastapi import APIRouter, HTTPException, Query
from geopy.distance import geodesic
from typing import List, Dict

router = APIRouter()

# Setup base directory for data
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOS_DATA_DIR = os.path.join(BASE_DIR, "sos", "data")

@router.get("/nearest-police-stations")
async def nearest_police_stations(
    lat: float,
    lon: float,
    top: int = Query(3, gt=0)
):
    data_path = os.path.join(SOS_DATA_DIR, "INDIA_POLICE_STATIONS.geojson")
    if not os.path.exists(data_path):
        raise HTTPException(status_code=500, detail="Police station data not found")

    with open(data_path, "r", encoding="utf-8") as file:
        police_data = json.load(file)

    user_location = (lat, lon)
    distances = []

    for feature in police_data["features"]:
        coords = feature["geometry"]["coordinates"]
        # GeoJSON is [lon, lat], geopy needs [lat, lon]
        station_location = (coords[1], coords[0])
        distance_km = geodesic(user_location, station_location).kilometers

        distances.append({
            "name": feature["properties"]["ps"],
            "state": feature["properties"]["state"],
            "district": feature["properties"]["district"],
            "coordinates": station_location,
            "distance_km": round(distance_km, 2)
        })

    distances.sort(key=lambda x: x["distance_km"])
    return distances[:top]

@router.get("/crime-data")
async def get_crime_data():
    json_path = os.path.join(SOS_DATA_DIR, "crime_clusters.geojson")
    if not os.path.exists(json_path):
        raise HTTPException(status_code=500, detail="Crime data not found")

    with open(json_path, encoding="utf-8") as f:
        geojson = json.load(f)
    
    records = []
    for feature in geojson["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        record = {
            "Longitude": coords[0],
            "Latitude": coords[1],
            "attack type": props.get("attack type", ""),
            "city": props.get("city", ""),
            "day": props.get("day", ""),
            "location": props.get("location", ""),
            "month": props.get("month", ""),
            "state": props.get("state", ""),
            "summary": props.get("summary", ""),
            "year": props.get("year", "")
        }
        records.append(record)
    return records
