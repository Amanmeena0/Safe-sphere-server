from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class MissingPersonCreate(BaseModel):
    name: str
    number_of_person: int
    nick_name: str
    father_name: str
    relation: str
    last_known_address: str
    gender: Optional[str] = None
    year_of_birth: int
    age_from: int
    age_to: int
    body_build: str
    complexion: str
    weight: float
    height_range: float
    incident_report: str
    details_last_seen: str
    date_time_last_seen: datetime
    complainant_name: str
    relation_with_missing_person: str
    complainant_address: str
    complainant_contact: str
    alternate_number: str
    email_address: str
    any_other_details: str
    police_station: str
    complainant_district: str
    image: Optional[bytes] = b'' # Needs multipart form support eventually if it's file upload
