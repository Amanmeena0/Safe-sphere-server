from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from app.api.dependencies import get_db, get_current_user
from app.services.user_service import UserService
from app.services.fir_service import FIRService
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

@router.get("/firs")
async def get_my_firs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch all types of reports submitted by the authenticated citizen.
    """
    service = FIRService(db)
    return service.get_user_reports(current_user.clerk_user_id)

@router.get("/sos")
async def get_my_sos_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Fetch all SOS reports submitted by the authenticated user.
    """
    from app.services.sos_service import SOSService
    service = SOSService()
    return service.get_user_sos_reports(db, current_user.clerk_user_id)
