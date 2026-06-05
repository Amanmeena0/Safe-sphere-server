from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.models.models import User, cyberCrime, theftEfir, LostItem, missingPerson, domesticForm, rapecase, mvTheft

router = APIRouter()

@router.get("/api/profile")
async def get_profile(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        user = db.query(User).filter(User.auth_id == user_id).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = {
            "id": user.id,
            "auth_id": user.auth_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "role": user.role,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "emergency_contact_name": user.emergency_contact_name,
            "emergency_contact_phone": user.emergency_contact_phone,
            "registration_date": user.registration_date.isoformat() if user.registration_date else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "status": user.status
        }
        return user_data

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")

@router.get("/api/profile/my-firs")
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

@router.delete("/api/profile")
async def delete_profile(
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        user = db.query(User).filter(User.auth_id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return {"message": "User profile deleted successfully."}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error occurred: {str(e)}")
