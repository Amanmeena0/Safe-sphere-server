# app/models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    address = db.Column(db.String(255))
    aadhar_number = db.Column(db.String(12), unique=True)
    role = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(15))
    registration_date = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    status = db.Column(db.String(20))


class LostItem(db.Model):
    __tablename__ = 'lost_items'

    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.String(255), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    placeofloss = db.Column(db.String(255))
    loss_datetime = db.Column(db.DateTime, nullable=False)
    owner_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(255))
    document_type = db.Column(db.String(512), nullable=False)
    police_station = db.Column(db.String(100))
    district = db.Column(db.String(100))

class cyberCrime(db.Model):
    __tablename__ = 'cyber_crimes'

    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.String(255), nullable=False)
    crimeCategory = db.Column(db.String(100), nullable=False)
    platform = db.Column(db.String(100))
    date_of_incident = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(50))
    IpAddress = db.Column(db.String(50))
    description = db.Column(db.Text, nullable=False)
    digitalEvidence = db.Column(db.String(512), default='')
    full_name = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    relation = db.Column(db.String(50))
    policeStation = db.Column(db.String(100), nullable=False)

class rapecase(db.Model):
    __tablename__ = 'rape_cases'

    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.String(255), nullable=False)
    victim_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    incidentDetails = db.Column(db.Text, nullable=False)
    perpetratorDetails = db.Column(db.Text, nullable=False)
    location_of_incident = db.Column(db.String(255), nullable=False)
    date_of_incident = db.Column(db.Date, nullable=False)
    time_of_incident = db.Column(db.String(50), nullable=False)
    upload_document = db.Column(db.String(512), default='')
    informant_details = db.Column(db.Text, nullable=False)
    police_station = db.Column(db.String(100), nullable=False)


class domesticForm(db.Model):
    __tablename__ = 'domestic_forms'

    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.String(255), nullable=False)
    registeration_type = db.Column(db.String(100), nullable=False)
    reporter_details = db.Column(db.Text, nullable=False)
    reporter_age = db.Column(db.Integer)
    reporter_gender = db.Column(db.String(10))
    reporter_contact = db.Column(db.String(15))
    reporter_Emailaddress = db.Column(db.String(255), nullable=False)
    reporter_native_place = db.Column(db.String(255), nullable=False)
    employer_name = db.Column(db.String(100), nullable=False)
    employer_contact = db.Column(db.String(15), nullable=False)
    employer_relations = db.Column(db.String(100), nullable=False)
    employer_address = db.Column(db.String(255), nullable=False)
    documentation = db.Column(db.String(512), default='')
    duration_of_stay = db.Column(db.String(100), nullable=False)


class theftEfir(db.Model):
    __tablename__ = 'theft_efirs'

    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.String(255), nullable=False)
    incident_description = db.Column(db.Text, nullable=False)
    date_of_theft = db.Column(db.Date, nullable=False)
    financial_impact = db.Column(db.Text)
    witness_information = db.Column(db.Text)
    complainant_details = db.Column(db.Text)
    upload_document = db.Column(db.String(512), default='')
    police_station = db.Column(db.String(100), nullable=False)

class mvTheft(db.Model):
    __tablename__ = 'mv_thefts'

    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.String(255), nullable=False)
    vehicleDetails = db.Column(db.Text, nullable=False)
    owner_details = db.Column(db.Text, nullable=False)
    date_of_theft = db.Column(db.Date, nullable=False)
    timeoftheft = db.Column(db.String(50), nullable=False)
    location_of_theft = db.Column(db.String(255), nullable=False)
    previous_fir_details = db.Column(db.Text, nullable=False)
    upload_document = db.Column(db.String(512), default='')
    police_station = db.Column(db.String(100), nullable=False)


class missingPerson(db.Model):
    __tablename__ = 'missing_persons'

    id = db.Column(db.Integer, primary_key=True)
    user_auth_id = db.Column(db.String(255), nullable=False)
    Fullname = db.Column(db.String(100), nullable=False)
    Numberofperson = db.Column(db.Integer, nullable=False)
    nickname = db.Column(db.String(100), nullable=False)
    fathername = db.Column(db.String(100), nullable=False)
    relation = db.Column(db.String(100), nullable=False)
    lastknownlocation = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.String(10))
    yearofbirth = db.Column(db.Integer, nullable=False)
    agefrom = db.Column(db.Integer, nullable=False)
    ageto = db.Column(db.Integer, nullable=False)
    bodybuild = db.Column(db.String(100), nullable=False)
    complexion = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    incidentReport = db.Column(db.Text, nullable=False)
    detailsLastseen = db.Column(db.Text, nullable=False)
    datetimelastseen = db.Column(db.DateTime, nullable=False)
    complainant_name = db.Column(db.Text, nullable=False)
    relationwithMissingperson = db.Column(db.String(100), nullable=False)
    complainant_address = db.Column(db.String(255), nullable=False)
    complainant_contact = db.Column(db.String(15), nullable=False)
    alternate_contact = db.Column(db.String(15), nullable=False)
    emailaddress = db.Column(db.String(255), nullable=False)
    anyotherdetails = db.Column(db.Text, nullable=False)
    policestation = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    upload_document = db.Column(db.String(512), default='')