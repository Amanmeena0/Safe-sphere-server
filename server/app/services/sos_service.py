import os
import json
from fastapi import HTTPException
from geopy.distance import geodesic
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.models import SOSReport
from app.schemas.sos import SOSReportCreate

class SOSService:
    _POLICE_STATIONS_CACHE = None
    _CRIME_CLUSTERS_CACHE = None

    def __init__(self):
        # Setup base directory for data
        # __file__ is app/services/sos_service.py
        # app_dir is app/
        self.APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # root_dir is the project root
        self.ROOT_DIR = os.path.dirname(self.APP_DIR)
        self.SOS_DATA_DIR = os.path.join(self.ROOT_DIR, "app", "DataOfEverything") # Based on tree: app/DataOfEverything

    def _get_police_stations(self):
        if SOSService._POLICE_STATIONS_CACHE is None:
            data_path = os.path.join(self.SOS_DATA_DIR, "INDIA_POLICE_STATIONS.geojson")
            if not os.path.exists(data_path):
                raise HTTPException(status_code=500, detail="Police station data not found")
            with open(data_path, "r", encoding="utf-8") as file:
                SOSService._POLICE_STATIONS_CACHE = json.load(file)
        return SOSService._POLICE_STATIONS_CACHE

    def _get_crime_clusters(self):
        if SOSService._CRIME_CLUSTERS_CACHE is None:
            json_path = os.path.join(self.SOS_DATA_DIR, "crime_clusters.geojson")
            if not os.path.exists(json_path):
                raise HTTPException(status_code=500, detail="Crime data not found")
            with open(json_path, encoding="utf-8") as f:
                SOSService._CRIME_CLUSTERS_CACHE = json.load(f)
        return SOSService._CRIME_CLUSTERS_CACHE

    def get_nearest_police_stations(self, lat: float, lon: float, top: int = 3) -> List[Dict]:
        police_data = self._get_police_stations()
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

    def get_crime_data(self) -> List[Dict]:
        geojson = self._get_crime_clusters()
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
            print(f"SOS Triggered by {auth_id} at {db_sos.timestamp}")
            
            return db_sos
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to save SOS report: {str(e)}")
