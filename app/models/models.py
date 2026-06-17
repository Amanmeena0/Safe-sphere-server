from sqlalchemy import Column, Integer, String, Date, DateTime, Text, Float, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clerk_user_id = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(100), index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    name = Column(String(200)) # Keep for compatibility or combine first/last
    status = Column(String(50), default="active")
    registration_date = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class LostItem(Base):
    __tablename__ = 'lost_items'

    auth_id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String(255), nullable=False)
    item_name = Column(String(100), nullable=False)
    brand = Column(String(100))
    model = Column(String(100))
    placeofloss = Column(String(255))
    loss_datetime = Column(DateTime, nullable=False)
    owner_name = Column(String(100), nullable=False)
    contact_number = Column(String(15), nullable=False)
    address = Column(String(255))
    document_type = Column(Text, nullable=False)
    police_station = Column(String(100))
    district = Column(String(100))

class cyberCrime(Base):
    __tablename__ = 'cyber_crimes'

    auth_id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String(255), nullable=False)
    crimeCategory = Column(String(100), nullable=False)
    platform = Column(String(100))
    date_of_incident = Column(Date, nullable=False)
    time = Column(String(50))
    IpAddress = Column(String(50))
    description = Column(Text, nullable=False)
    digitalEvidence = Column(Text, default='')
    full_name = Column(String(100), nullable=False)
    contact_number = Column(String(15), nullable=False)
    email = Column(String(100))
    address = Column(String(255), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    relation = Column(String(50))
    police_station = Column(String(100), nullable=False)

class rapecase(Base):
    __tablename__ = 'rape_cases'

    auth_id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String(255), nullable=False)
    victim_name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    incidentDetails = Column(Text, nullable=False)
    perpetratorDetails = Column(Text, nullable=False)
    location_of_incident = Column(String(255), nullable=False)
    date_of_incident = Column(Date, nullable=False)
    time_of_incident = Column(String(50), nullable=False)
    upload_document = Column(Text, default='')
    informant_details = Column(Text, nullable=False)
    police_station = Column(String(100), nullable=False)


class domesticForm(Base):
    __tablename__ = 'domestic_forms'

    auth_id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String(255), nullable=False)
    registeration_type = Column(String(100), nullable=False)
    reporter_details = Column(Text, nullable=False)
    reporter_age = Column(Integer)
    reporter_gender = Column(String(10))
    reporter_contact = Column(String(15))
    reporter_Emailaddress = Column(String(255), nullable=False)
    reporter_native_place = Column(String(255), nullable=False)
    employer_name = Column(String(100), nullable=False)
    employer_contact = Column(String(15), nullable=False)
    employer_relations = Column(String(100), nullable=False)
    employer_address = Column(String(255), nullable=False)
    documentation = Column(Text, default='')
    duration_of_stay = Column(String(100), nullable=False)
    police_station = Column(String(100), nullable=False)


class theftEfir(Base):
    __tablename__ = 'theft_efirs'

    auth_id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String(255), nullable=False)
    incident_description = Column(Text, nullable=False)
    date_of_theft = Column(Date, nullable=False)
    financial_impact = Column(Text)
    witness_information = Column(Text)
    complainant_details = Column(Text)
    upload_document = Column(Text, default='')
    police_station = Column(String(100), nullable=False)

class mvTheft(Base):
    __tablename__ = 'mv_thefts'

    auth_id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String(255), nullable=False)
    vehicleDetails = Column(Text, nullable=False)
    owner_details = Column(Text, nullable=False)
    date_of_theft = Column(Date, nullable=False)
    timeoftheft = Column(String(50), nullable=False)
    location_of_theft = Column(String(255), nullable=False)
    previous_fir_details = Column(Text, nullable=False)
    upload_document = Column(Text, default='')
    police_station = Column(String(100), nullable=False)


class missingPerson(Base):
    __tablename__ = 'missing_persons'

    auth_id = Column(Integer, primary_key=True)
    clerk_user_id = Column(String(255), nullable=False)
    Fullname = Column(String(100), nullable=False)
    Numberofperson = Column(Integer, nullable=False)
    nickname = Column(String(100), nullable=False)
    fathername = Column(String(100), nullable=False)
    relation = Column(String(100), nullable=False)
    lastknownlocation = Column(String(255), nullable=False)
    gender = Column(String(10))
    yearofbirth = Column(Integer, nullable=False)
    agefrom = Column(Integer, nullable=False)
    ageto = Column(Integer, nullable=False)
    bodybuild = Column(String(100), nullable=False)
    complexion = Column(String(100), nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    incidentReport = Column(Text, nullable=False)
    detailsLastseen = Column(Text, nullable=False)
    datetimelastseen = Column(DateTime, nullable=False)
    complainant_name = Column(Text, nullable=False)
    relationwithMissingperson = Column(String(100), nullable=False)
    complainant_address = Column(String(255), nullable=False)
    complainant_contact = Column(String(15), nullable=False)
    alternate_contact = Column(String(15), nullable=False)
    emailaddress = Column(String(255), nullable=False)
    anyotherdetails = Column(Text, nullable=False)
    police_station = Column(String(100), nullable=False)
    district = Column(String(100), nullable=False)
    upload_document = Column(Text, default='')

class SOSReport(Base):
    __tablename__ = 'sos_reports'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    clerk_user_id = Column(String(255), nullable=False, index=True)
    location_address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    incident_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), default='active')
    timestamp = Column(DateTime, default=func.now())

class CrimeData(Base):
    __tablename__ = 'crime_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    state_ut = Column(String(255), index=True)
    district = Column(String(255), index=True)
    year = Column(Integer, index=True)
    murder = Column(Integer)
    attempt_to_murder = Column(Integer)
    culpable_homicide_not_amounting_to_murder = Column(Integer)
    rape = Column(Integer)
    custodial_rape = Column(Integer)
    other_rape = Column(Integer)
    kidnapping_abduction = Column(Integer)
    kidnapping_and_abduction_of_women_and_girls = Column(Integer)
    kidnapping_and_abduction_of_others = Column(Integer)
    dacoity = Column(Integer)
    preparation_and_assembly_for_dacoity = Column(Integer)
    robbery = Column(Integer)
    burglary = Column(Integer)
    theft = Column(Integer)
    auto_theft = Column(Integer)
    other_theft = Column(Integer)
    riots = Column(Integer)
    criminal_breach_of_trust = Column(Integer)
    cheating = Column(Integer)
    counterfeiting = Column(Integer)
    arson = Column(Integer)
    hurt_grevious_hurt = Column(Integer)
    dowry_deaths = Column(Integer)
    assault_on_women_with_intent_to_outrage_her_modesty = Column(Integer)
    insult_to_modesty_of_women = Column(Integer)
    cruelty_by_husband_or_his_relatives = Column(Integer)
    importation_of_girls_from_foreign_countries = Column(Integer)
    causing_death_by_negligence = Column(Integer)
    other_ipc_crimes = Column(Integer)
    total_ipc_crimes = Column(Integer)
