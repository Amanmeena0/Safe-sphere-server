from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from app.api.dependencies import get_db, get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models.models import User, cyberCrime, theftEfir, LostItem, missingPerson, domesticForm, rapecase, mvTheft, SOSReport
from app.utils.redis_client import get_redis

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Explicit registration endpoint. 
    Note: get_current_user now handles auto-sync, but this remains for manual registration if needed.
    """
    service = UserService(db)
    # Map old auth_id to new clerk_user_id if provided in legacy payloads
    if hasattr(user_data, 'auth_id') and not user_data.clerk_user_id:
        user_data.clerk_user_id = user_data.auth_id
        
    return service.get_or_create_user(user_data.clerk_user_id)

@router.get("/check")
async def check_profile(
    current_user: User = Depends(get_current_user),
    redis = Depends(get_redis)
):
    # Since get_current_user ensures the user exists, we can return True
    return {
        "exists": True, 
        "profile_completed": True,
        "user_data": {
            "name": current_user.name,
            "email": current_user.email,
            "registration_date": current_user.registration_date.isoformat() if current_user.registration_date else None
        }
    }

@router.get("/me", response_model=UserResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    redis = Depends(get_redis)
):
    service = UserService(db)
    updated_user = service.update_profile(current_user.clerk_user_id, update_data)
    
    # Invalidate existing caches
    redis.delete(f"user_profile:{current_user.clerk_user_id}")
    redis.delete(f"user_check:{current_user.clerk_user_id}")
    
    return updated_user

@router.get("/my-firs")
async def get_my_firs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch all types of reports submitted by the authenticated citizen.
    """
    try:
        user_id = current_user.clerk_user_id
        def serialize(items):
            return [{c.name: getattr(item, c.name) for c in item.__table__.columns} for item in items]

        data = {
            "cyber_crimes": serialize(db.query(cyberCrime).filter(cyberCrime.clerk_user_id == user_id).all()),
            "theft_efirs": serialize(db.query(theftEfir).filter(theftEfir.clerk_user_id == user_id).all()),
            "lost_items": serialize(db.query(LostItem).filter(LostItem.clerk_user_id == user_id).all()),
            "missing_persons": serialize(db.query(missingPerson).filter(missingPerson.clerk_user_id == user_id).all()),
            "domestic_forms": serialize(db.query(domesticForm).filter(domesticForm.clerk_user_id == user_id).all()),
            "rape_cases": serialize(db.query(rapecase).filter(rapecase.clerk_user_id == user_id).all()),
            "mv_thefts": serialize(db.query(mvTheft).filter(mvTheft.clerk_user_id == user_id).all()),
            "sos_reports": serialize(db.query(SOSReport).filter(SOSReport.clerk_user_id == user_id).all())
        }

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {str(e)}")

@router.get("/sos")
async def get_my_sos_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch all SOS reports submitted by the authenticated user.
    """
    try:
        user_id = current_user.clerk_user_id
        reports = db.query(SOSReport).filter(SOSReport.clerk_user_id == user_id).all()
        return [{c.name: getattr(report, c.name) for c in report.__table__.columns} for report in reports]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch SOS reports: {str(e)}")
