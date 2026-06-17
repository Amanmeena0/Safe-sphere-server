import os
import json
import requests
from fastapi import HTTPException
from typing import Optional, List, Dict
from pathlib import Path
from sqlalchemy.orm import Session
from app.repositories.crime_repository import CrimeRepository

class CrimeService:
    _CRIME_CLUSTERS_CACHE = None

    def __init__(self, db: Optional[Session] = None):
        if db:
            self.repository = CrimeRepository(db)
        
        # Setup base directory for local fallback
        current_file = Path(__file__).resolve()
        potential_root = current_file.parent.parent.parent
        self.DATA_DIR = potential_root / "store"
        
        if not self.DATA_DIR.exists():
            self.DATA_DIR = Path.cwd() / "store"
            
        self.CRIME_CLUSTERS_URL = os.getenv("CRIME_CLUSTERS_URL")

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

    def _get_crime_clusters(self):
        if CrimeService._CRIME_CLUSTERS_CACHE is None:
            CrimeService._CRIME_CLUSTERS_CACHE = self._fetch_data(
                self.CRIME_CLUSTERS_URL, 
                "crime_clusters.geojson"
            )
        return CrimeService._CRIME_CLUSTERS_CACHE

    def get_crime_clusters(self) -> List[Dict]:
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
                    
                    record = {
                        "longitude": coords[0],
                        "latitude": coords[1],
                        "incident_type": props.get("attack type", props.get("incident_type", "Unknown")),
                        "city": props.get("city", "Unknown"),
                        "district": props.get("city", "Unknown"),
                        "day": props.get("day", ""),
                        "location": props.get("location", ""),
                        "month": props.get("month", ""),
                        "state": props.get("state", "Unknown"),
                        "state_ut": props.get("state", "Unknown"),
                        "summary": props.get("summary", ""),
                        "year": props.get("year", "")
                    }
                    records.append(record)
                except (IndexError, TypeError, KeyError):
                    continue
            return records
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process crime data: {str(e)}")

    def search_crime(
        self,
        state_ut: Optional[str] = None,
        district: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict]:
        if not hasattr(self, 'repository'):
            raise HTTPException(status_code=500, detail="Database session not initialized for CrimeService")
        return self.repository.search_crime_data(
            state_ut=state_ut,
            district=district,
            year=year,
            limit=limit
        )
