from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

class FIRBase(BaseModel):
    user_auth_id: str
    police_station: str

class LostItemCreate(FIRBase):
    item_name: str
    brand: Optional[str] = None
    model: Optional[str] = None
    placeofloss: str
    loss_datetime: datetime
    owner_name: str
    contact_number: str
    address: Optional[str] = None
    document_type: str
    district: str

class CyberCrimeCreate(FIRBase):
    crimeCategory: str
    platform: Optional[str] = None
    date_of_incident: date
    time: Optional[str] = None
    IpAddress: Optional[str] = None
    description: str
    digitalEvidence: Optional[str] = ""
    full_name: str
    contact_number: str
    email: Optional[str] = None
    address: str
    age: Optional[int] = None
    gender: Optional[str] = None
    relation: Optional[str] = None

class RapeCaseCreate(FIRBase):
    victim_name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    incidentDetails: str
    perpetratorDetails: str
    location_of_incident: str
    date_of_incident: date
    time_of_incident: str
    upload_document: Optional[str] = ""
    informant_details: str

class DomesticFormCreate(FIRBase):
    registeration_type: str
    reporter_details: str
    reporter_age: Optional[int] = None
    reporter_gender: Optional[str] = None
    reporter_contact: Optional[str] = None
    reporter_Emailaddress: str
    reporter_native_place: str
    employer_name: str
    employer_contact: str
    employer_relations: str
    employer_address: str
    documentation: Optional[str] = ""
    duration_of_stay: str

class TheftEfirCreate(FIRBase):
    incident_description: str
    date_of_theft: date
    financial_impact: Optional[str] = None
    witness_information: Optional[str] = None
    complainant_details: Optional[str] = None
    upload_document: Optional[str] = ""

class MVTheftCreate(FIRBase):
    vehicleDetails: str
    owner_details: str
    date_of_theft: date
    timeoftheft: str
    location_of_theft: str
    previous_fir_details: str
    upload_document: Optional[str] = ""

class MissingPersonCreate(FIRBase):
    Fullname: str
    Numberofperson: int
    nickname: str
    fathername: str
    relation: str
    lastknownlocation: str
    gender: Optional[str] = None
    yearofbirth: int
    agefrom: int
    ageto: int
    bodybuild: str
    complexion: str
    weight: float
    height: float
    incidentReport: str
    detailsLastseen: str
    datetimelastseen: datetime
    complainant_name: str
    relationwithMissingperson: str
    complainant_address: str
    complainant_contact: str
    alternate_contact: str
    emailaddress: str
    anyotherdetails: str
    district: str
    upload_document: Optional[str] = ""
