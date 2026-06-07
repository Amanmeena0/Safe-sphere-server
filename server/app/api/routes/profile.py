from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
from app.api.dependencies import get_db, get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.models.models import cyberCrime, theftEfir, LostItem, missingPerson, domesticForm, rapecase, mvTheft
from app.utils.redis_client import get_redis

router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    service = UserService(db)
    return service.register_user(user_data)

@router.get("/check")
async def check_profile(
    db: Session = Depends(get_db),
    auth_id: str = Depends(get_current_user),
    redis = Depends(get_redis)
):
    # Try fetching from cache first
    cache_key = f"user_check:{auth_id}"
    cached_data = redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    service = UserService(db)
    try:
        user = service.get_profile(auth_id)
        response_data = {
            "exists": True,
            "profile_completed": True,
            "role": user.role,
            "user_data": {
                "name": user.name,
                "email": user.email,
                "registration_date": user.registration_date.isoformat() if user.registration_date else None
            }
        }
        # Cache the result for 1 hour
        redis.set(cache_key, json.dumps(response_data), ex=3600)
        return response_data
    except HTTPException as e:
        if e.status_code == 404:
            return {"exists": False, "profile_completed": False}
        raise e

@router.get("/me")
async def get_my_profile(
    db: Session = Depends(get_db),
    auth_id: str = Depends(get_current_user),
    redis = Depends(get_redis)
):
    # Try fetching from cache first
    cache_key = f"user_profile:{auth_id}"
    cached_data = redis.get(cache_key)
    if cached_data:
        return json.loads(cached_data)

    service = UserService(db)
    user = service.get_profile(auth_id)
    
    # Serialize the user object (assuming it has a way to be converted to dict or just pick fields)
    # For now, let's assume service.get_profile returns a pydantic-compatible model or we manually build it
    user_data = {
        "id": user.id,
        "auth_id": user.auth_id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "registration_date": user.registration_date.isoformat() if user.registration_date else None
    }
    
    # Cache the result for 1 hour
    redis.set(cache_key, json.dumps(user_data), ex=3600)
    return user_data

@router.put("/me")
async def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    auth_id: str = Depends(get_current_user),
    redis = Depends(get_redis)
):
    service = UserService(db)
    updated_user = service.update_profile(auth_id, update_data)
    
    # Invalidate existing caches
    redis.delete(f"user_profile:{auth_id}")
    redis.delete(f"user_check:{auth_id}")
    
    return updated_user

@router.get("/my-firs")
async def get_my_firs(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    """
    Fetch all types of reports submitted by the authenticated citizen.
    """
    try:
        def serialize(items):
            return [{c.name: getattr(item, c.name) for c in item.__table__.columns} for item in items]

        data = {
            "cyber_crimes": serialize(db.query(cyberCrime).filter(cyberCrime.user_auth_id == user_id).all()),
            "theft_efirs": serialize(db.query(theftEfir).filter(theftEfir.user_auth_id == user_id).all()),
            "lost_items": serialize(db.query(LostItem).filter(LostItem.user_auth_id == user_id).all()),
            "missing_persons": serialize(db.query(missingPerson).filter(missingPerson.user_auth_id == user_id).all()),
            "domestic_forms": serialize(db.query(domesticForm).filter(domesticForm.user_auth_id == user_id).all()),
            "rape_cases": serialize(db.query(rapecase).filter(rapecase.user_auth_id == user_id).all()),
            "mv_thefts": serialize(db.query(mvTheft).filter(mvTheft.user_auth_id == user_id).all())
        }

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {str(e)}")
