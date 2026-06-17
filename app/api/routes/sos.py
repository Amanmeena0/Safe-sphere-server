from fastapi import APIRouter, Query, Depends, status
from sqlalchemy.orm import Session
from app.services.sos_service import SOSService
from app.schemas.sos import SOSReportCreate, SOSReportResponse
from app.api.dependencies import get_db, get_current_user
from app.models.models import User

router = APIRouter()
sos_service = SOSService()

@router.get("/nearest-police-stations")
@router.get("/stations")
async def nearest_police_stations(
    lat: float,
    lon: float,
    top: int = Query(3, gt=0)
):
    return sos_service.get_nearest_police_stations(lat, lon, top)

@router.get("/crime-data")
@router.get("/clusters")
async def get_crime_data():
    return sos_service.get_crime_data()

@router.post("/trigger", response_model=SOSReportResponse, status_code=status.HTTP_201_CREATED)
async def trigger_sos(
    sos_data: SOSReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return sos_service.trigger_sos(db, sos_data, current_user.clerk_user_id)
