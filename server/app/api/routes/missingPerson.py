from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.dependencies import get_db, get_current_user
from app.models.models import missingPerson
from app.schemas.forms import MissingPersonCreate

router = APIRouter()

@router.post("/api/firs/missing_person", status_code=status.HTTP_201_CREATED)
async def report_missing_person(
    data: MissingPersonCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    try:
        new_missing_person = missingPerson(
            user_auth_id=user_id,
            Fullname=data.name,
            Numberofperson=data.number_of_person,
            nickname=data.nick_name,
            fathername=data.father_name,
            relation=data.relation,
            lastknownlocation=data.last_known_address,
            gender=data.gender,
            yearofbirth=data.year_of_birth,
            agefrom=data.age_from,
            ageto=data.age_to,
            bodybuild=data.body_build,
            complexion=data.complexion,
            weight=data.weight,
            height=data.height_range,
            incidentReport=data.incident_report,
            detailsLastseen=data.details_last_seen,
            datetimelastseen=data.date_time_last_seen,
            complainant_name=data.complainant_name,
            relationwithMissingperson=data.relation_with_missing_person,
            complainant_address=data.complainant_address,
            complainant_contact=data.complainant_contact,
            alternate_contact=data.alternate_number,
            emailaddress=data.email_address,
            anyotherdetails=data.any_other_details,
            policestation=data.police_station,
            district=data.complainant_district,
            upload_document=data.image.decode('utf-8') if data.image else '', # Assuming text for now based on model
        )
        db.add(new_missing_person)
        db.commit()
        return {"message": "Missing person reported successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
