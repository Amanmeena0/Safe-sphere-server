import os
import json
import math
import requests
from fastapi import HTTPException
from typing import List, Dict
from pathlib import Path

class PoliceService:
    _POLICE_STATIONS_CACHE = None

    def __init__(self):
        # Setup base directory for local fallback
        current_file = Path(__file__).resolve()
        
        # Check parent of parent (root/app/services/police_service.py -> root/store)
        potential_root = current_file.parent.parent.parent
        self.DATA_DIR = potential_root / "store"
        
        if not self.DATA_DIR.exists():
            self.DATA_DIR = Path.cwd() / "store"
            
        self.POLICE_STATIONS_URL = os.getenv("POLICE_STATIONS_URL")

    def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers
        return c * r

    def _fetch_data(self, url: str, local_filename: str):
        if url:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Warning: Failed to fetch remote data from {url}: {e}")
        
        local_path = self.DATA_DIR / local_filename
        if not local_path.exists():
            fallback_path = Path(__file__).resolve().parent.parent.parent / "store" / local_filename
            if fallback_path.exists():
                local_path = fallback_path
            else:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Data file {local_filename} not found."
                )
            
        with open(local_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _get_police_stations(self):
        if PoliceService._POLICE_STATIONS_CACHE is None:
            PoliceService._POLICE_STATIONS_CACHE = self._fetch_data(
                self.POLICE_STATIONS_URL, 
                "INDIA_POLICE_STATIONS.geojson"
            )
        return PoliceService._POLICE_STATIONS_CACHE

    def get_nearest_police_stations(self, lat: float, lon: float, top: int = 3) -> List[Dict]:
        try:
            police_data = self._get_police_stations()
            if not police_data or "features" not in police_data:
                return []
                
            distances = []

            for feature in police_data["features"]:
                try:
                    geometry = feature.get("geometry", {})
                    coords = geometry.get("coordinates", [])
                    if len(coords) < 2:
                        continue
                        
                    station_lat, station_lon = coords[1], coords[0]
                    distance_km = self._haversine(lat, lon, station_lat, station_lon)

                    props = feature.get("properties", {})
                    distances.append({
                        "name": props.get("ps", "Unknown Station"),
                        "state": props.get("state", "Unknown State"),
                        "district": props.get("district", "Unknown District"),
                        "coordinates": (station_lat, station_lon),
                        "distance_km": round(distance_km, 2)
                    })
                except (IndexError, TypeError, KeyError):
                    continue

            distances.sort(key=lambda x: x["distance_km"])
            return distances[:top]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process police station data: {str(e)}")
