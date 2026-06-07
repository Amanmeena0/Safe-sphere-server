from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate
from app.models.models import cyberCrime, theftEfir, LostItem, missingPerson, domesticForm, rapecase, mvTheft

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
    auth_id: str = Depends(get_current_user)
):
    service = UserService(db)
    try:
        user = service.get_profile(auth_id)
        return {
            "exists": True,
            "profile_completed": True,
            "role": user.role,
            "user_data": {
                "name": user.name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "registration_date": user.registration_date.isoformat() if user.registration_date else None
            }
        }
    except HTTPException as e:
        if e.status_code == 404:
            return {"exists": False, "profile_completed": False}
        raise e

@router.get("/me")
async def get_my_profile(
    db: Session = Depends(get_db),
    auth_id: str = Depends(get_current_user)
):
    service = UserService(db)
    return service.get_profile(auth_id)

@router.put("/me")
async def update_my_profile(
    update_data: UserUpdate,
    db: Session = Depends(get_db),
    auth_id: str = Depends(get_current_user)
):
    service = UserService(db)
    return service.update_profile(auth_id, update_data)

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
