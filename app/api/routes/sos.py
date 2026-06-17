from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.services.sos_service import SOSService
from app.schemas.sos import SOSReportCreate, SOSReportResponse
from app.api.dependencies import get_db, get_current_user
from app.models.models import User

router = APIRouter()
sos_service = SOSService()

@router.post("/trigger", response_model=SOSReportResponse, status_code=status.HTTP_201_CREATED)
async def trigger_sos(
    sos_data: SOSReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Trigger an SOS signal and save it to the database.
    """
    return sos_service.trigger_sos(db, sos_data, current_user.clerk_user_id)
