import os
import json
import math
import requests
from fastapi import HTTPException
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.models import SOSReport
from app.schemas.sos import SOSReportCreate

from pathlib import Path

class SOSService:
    _POLICE_STATIONS_CACHE = None
    _CRIME_CLUSTERS_CACHE = None

    def __init__(self):
        # Setup base directory for local fallback
        # Try to find 'store' directory in several places
        current_file = Path(__file__).resolve()
        
        # 1. Check parent of parent (root/app/services/sos_service.py -> root/store)
        potential_root = current_file.parent.parent.parent
        self.SOS_DATA_DIR = potential_root / "store"
        
        # 2. Fallback to current working directory if not found
        if not self.SOS_DATA_DIR.exists():
            self.SOS_DATA_DIR = Path.cwd() / "store"
            
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
        local_path = self.SOS_DATA_DIR / local_filename
        if not local_path.exists():
            # Try one last fallback: relative to app root
            fallback_path = Path(__file__).resolve().parent.parent.parent / "store" / local_filename
            if fallback_path.exists():
                local_path = fallback_path
            else:
                raise HTTPException(
                    status_code=500, 
                    detail=f"Data file {local_filename} not found. Looked in: {self.SOS_DATA_DIR} and {fallback_path.parent}"
                )
            
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
        try:
            police_data = self._get_police_stations()
            if not police_data or "features" not in police_data:
                return []
                
            user_location = (lat, lon)
            distances = []

            for feature in police_data["features"]:
                try:
                    geometry = feature.get("geometry", {})
                    coords = geometry.get("coordinates", [])
                    if len(coords) < 2:
                        continue
                        
                    # GeoJSON is [lon, lat], _haversine needs [lat1, lon1, lat2, lon2]
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
                except (IndexError, TypeError, KeyError) as e:
                    continue

            distances.sort(key=lambda x: x["distance_km"])
            return distances[:top]
        except Exception as e:
            print(f"Error in get_nearest_police_stations: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process police station data: {str(e)}")

    def get_crime_data(self) -> List[Dict]:
        try:
            geojson = self._get_crime_clusters()
            if not geojson or "features" not in geojson:
                return []
                
            records = []
            for feature in geojson["features"]:
                try:
                    props = feature.get("properties", {})
                    geometry = feature.get("geometry", {})
                    coords = geometry.get("coordinates", [0, 0])
                    
                    # Normalize keys to be consistent with SOSReport model and frontend expectations
                    record = {
                        "longitude": coords[0],
                        "latitude": coords[1],
                        "incident_type": props.get("attack type", props.get("incident_type", "Unknown")),
                        "city": props.get("city", "Unknown"),
                        "district": props.get("city", "Unknown"), # Alias for normalization
                        "day": props.get("day", ""),
                        "location": props.get("location", ""),
                        "month": props.get("month", ""),
                        "state": props.get("state", "Unknown"),
                        "state_ut": props.get("state", "Unknown"), # Alias for normalization
                        "summary": props.get("summary", ""),
                        "year": props.get("year", "")
                    }
                    records.append(record)
                except (IndexError, TypeError, KeyError):
                    continue
            return records
        except Exception as e:
            print(f"Error in get_crime_data: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to process crime data: {str(e)}")

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
