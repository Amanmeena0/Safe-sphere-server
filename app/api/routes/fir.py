from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.services.fir_service import FIRService
from app.models.models import User
from app.schemas.fir import (
    LostItemCreate, CyberCrimeCreate, RapeCaseCreate, DomesticFormCreate,
    TheftEfirCreate, MVTheftCreate, MissingPersonCreate
)

router = APIRouter()

@router.post("/lost-item", status_code=status.HTTP_201_CREATED)
async def register_lost_item(
    data: LostItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.clerk_user_id = current_user.clerk_user_id
    service = FIRService(db)
    return service.register_lost_item(data)

@router.post("/cyber-crime", status_code=status.HTTP_201_CREATED)
async def register_cyber_crime(
    data: CyberCrimeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.clerk_user_id = current_user.clerk_user_id
    service = FIRService(db)
    return service.register_cyber_crime(data)

@router.post("/rape-case", status_code=status.HTTP_201_CREATED)
async def register_rape_case(
    data: RapeCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.clerk_user_id = current_user.clerk_user_id
    service = FIRService(db)
    return service.register_rape_case(data)

@router.post("/domestic-violence", status_code=status.HTTP_201_CREATED)
async def register_domestic_form(
    data: DomesticFormCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.clerk_user_id = current_user.clerk_user_id
    service = FIRService(db)
    return service.register_domestic_form(data)

@router.post("/theft-efir", status_code=status.HTTP_201_CREATED)
async def register_theft_efir(
    data: TheftEfirCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.clerk_user_id = current_user.clerk_user_id
    service = FIRService(db)
    return service.register_theft_efir(data)

@router.post("/mv-theft", status_code=status.HTTP_201_CREATED)
async def register_mv_theft(
    data: MVTheftCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.clerk_user_id = current_user.clerk_user_id
    service = FIRService(db)
    return service.register_mv_theft(data)

@router.post("/missing-person", status_code=status.HTTP_201_CREATED)
async def register_missing_person(
    data: MissingPersonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data.clerk_user_id = current_user.clerk_user_id
    service = FIRService(db)
    return service.register_missing_person(data)
