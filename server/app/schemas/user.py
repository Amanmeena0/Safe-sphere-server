from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    auth_id: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    registration_date: Optional[date] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    auth_id: Optional[str] = None
