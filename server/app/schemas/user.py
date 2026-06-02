from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    auth_id: str
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    aadhar_number: Optional[str] = Field(None, min_length=12, max_length=12)
    role: Optional[str] = "user"
    date_of_birth: Optional[date] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    auth_id: Optional[str] = None
