from fastapi import APIRouter, Query
from app.services.sos_service import SOSService

router = APIRouter()
sos_service = SOSService()

@router.get("/nearest-police-stations")
async def nearest_police_stations(
    lat: float,
    lon: float,
    top: int = Query(3, gt=0)
):
    return sos_service.get_nearest_police_stations(lat, lon, top)

@router.get("/crime-data")
async def get_crime_data():
    return sos_service.get_crime_data()
