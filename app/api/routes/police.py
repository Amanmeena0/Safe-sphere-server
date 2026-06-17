from fastapi import APIRouter, Query
from app.services.police_service import PoliceService

router = APIRouter()
police_service = PoliceService()

@router.get("/stations/nearest")
async def nearest_police_stations(
    lat: float,
    lon: float,
    top: int = Query(3, gt=0)
):
    """
    Get the nearest police stations based on latitude and longitude.
    """
    return police_service.get_nearest_police_stations(lat, lon, top)
