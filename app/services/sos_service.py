import os
import json
import math
import requests
from fastapi import HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.models import SOSReport
from app.schemas.sos import SOSReportCreate

class SOSService:
    _POLICE_STATIONS_CACHE = None
    _CRIME_CLUSTERS_CACHE = None

    def __init__(self):
        # Setup base directory for local fallback
        self.APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.ROOT_DIR = os.path.dirname(self.APP_DIR)
        self.SOS_DATA_DIR = os.path.join(self.ROOT_DIR, "store")
        
        # Remote URLs from environment (optional)
        self.POLICE_STATIONS_URL = os.getenv("POLICE_STATIONS_URL")
        self.CRIME_CLUSTERS_URL = os.getenv("CRIME_CLUSTERS_URL")

    def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # Convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

        # Haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        r = 6371 # Radius of earth in kilometers
        return c * r

    def _fetch_data(self, url: str, local_filename: str):
        """Helper to fetch data from URL or local file."""
        # Try remote first if URL exists
        if url:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                print(f"Warning: Failed to fetch remote data from {url}: {e}")
        
        # Fallback to local file
        local_path = os.path.join(self.SOS_DATA_DIR, local_filename)
        if not os.path.exists(local_path):
            raise HTTPException(status_code=500, detail=f"Data file {local_filename} not found locally or remotely")
            
        with open(local_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def _get_police_stations(self):
        if SOSService._POLICE_STATIONS_CACHE is None:
            SOSService._POLICE_STATIONS_CACHE = self._fetch_data(
                self.POLICE_STATIONS_URL, 
                "INDIA_POLICE_STATIONS.geojson"
            )
        return SOSService._POLICE_STATIONS_CACHE

    def _get_crime_clusters(self):
        if SOSService._CRIME_CLUSTERS_CACHE is None:
            SOSService._CRIME_CLUSTERS_CACHE = self._fetch_data(
                self.CRIME_CLUSTERS_URL, 
                "crime_clusters.geojson"
            )
        return SOSService._CRIME_CLUSTERS_CACHE

    def get_nearest_police_stations(self, lat: float, lon: float, top: int = 3) -> List[Dict]:
        police_data = self._get_police_stations()
        user_location = (lat, lon)
        distances = []

        for feature in police_data["features"]:
            coords = feature["geometry"]["coordinates"]
            # GeoJSON is [lon, lat], _haversine needs [lat1, lon1, lat2, lon2]
            station_lat, station_lon = coords[1], coords[0]
            distance_km = self._haversine(lat, lon, station_lat, station_lon)

            distances.append({
                "name": feature["properties"]["ps"],
                "state": feature["properties"]["state"],
                "district": feature["properties"]["district"],
                "coordinates": (station_lat, station_lon),
                "distance_km": round(distance_km, 2)
            })

        distances.sort(key=lambda x: x["distance_km"])
        return distances[:top]

    def get_crime_data(self) -> List[Dict]:
        geojson = self._get_crime_clusters()
        records = []
        for feature in geojson["features"]:
            props = feature["properties"]
            coords = feature["geometry"]["coordinates"]
            # Normalize keys to be consistent with SOSReport model and frontend expectations
            record = {
                "longitude": coords[0],
                "latitude": coords[1],
                "incident_type": props.get("attack type", props.get("incident_type", "")),
                "city": props.get("city", ""),
                "district": props.get("city", ""), # Alias for normalization
                "day": props.get("day", ""),
                "location": props.get("location", ""),
                "month": props.get("month", ""),
                "state": props.get("state", ""),
                "state_ut": props.get("state", ""), # Alias for normalization
                "summary": props.get("summary", ""),
                "year": props.get("year", "")
            }
            records.append(record)
        return records

    def trigger_sos(self, db: Session, sos_data: SOSReportCreate, clerk_user_id: str):
        try:
            db_sos = SOSReport(
                clerk_user_id=clerk_user_id,
                location_address=sos_data.location_address,
                latitude=sos_data.latitude,
                longitude=sos_data.longitude,
                incident_type=sos_data.incident_type,
                description=sos_data.description
            )
            db.add(db_sos)
            db.commit()
            db.refresh(db_sos)
            
            # Log the receipt of SOS signal
            print(f"SOS Triggered by {clerk_user_id} at {db_sos.timestamp}")
            
            return db_sos
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to save SOS report: {str(e)}")
