from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SOSReportBase(BaseModel):
    location_address: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    incident_type: str
    description: Optional[str] = None

class SOSReportCreate(SOSReportBase):
    pass

class SOSReportResponse(SOSReportBase):
    auth_id: str
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True
