from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.services.crime_service import CrimeService
from typing import Optional

router = APIRouter()

@router.get("/search")
async def search_crime(
    state_ut: Optional[str] = None,
    district: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = Query(50, gt=0),
    db: Session = Depends(get_db)
):
    """
    Search crime data from the database.
    """
    service = CrimeService(db)
    return service.search_crime(
        state_ut=state_ut,
        district=district,
        year=year,
        limit=limit
    )

@router.get("/clusters")
async def get_crime_clusters():
    """
    Get crime cluster data from GeoJSON.
    """
    service = CrimeService()
    return service.get_crime_clusters()
