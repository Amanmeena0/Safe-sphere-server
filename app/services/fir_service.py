from typing import Dict, List
from sqlalchemy.orm import Session
from app.repositories.fir_repository import FIRRepository
from app.schemas.fir import (
    LostItemCreate, CyberCrimeCreate, RapeCaseCreate, DomesticFormCreate,
    TheftEfirCreate, MVTheftCreate, MissingPersonCreate
)
from app.models.models import (
    LostItem, cyberCrime, rapecase, domesticForm, theftEfir, mvTheft, missingPerson, SOSReport
)

class FIRService:
    def __init__(self, db: Session):
        self.repository = FIRRepository(db)
        self.db = db

    def get_user_reports(self, user_id: str) -> Dict[str, List[Dict]]:
        def serialize(items):
            return [{c.name: getattr(item, c.name) for c in item.__table__.columns} for item in items]

        return {
            "cyber_crimes": serialize(self.db.query(cyberCrime).filter(cyberCrime.clerk_user_id == user_id).all()),
            "theft_efirs": serialize(self.db.query(theftEfir).filter(theftEfir.clerk_user_id == user_id).all()),
            "lost_items": serialize(self.db.query(LostItem).filter(LostItem.clerk_user_id == user_id).all()),
            "missing_persons": serialize(self.db.query(missingPerson).filter(missingPerson.clerk_user_id == user_id).all()),
            "domestic_forms": serialize(self.db.query(domesticForm).filter(domesticForm.clerk_user_id == user_id).all()),
            "rape_cases": serialize(self.db.query(rapecase).filter(rapecase.clerk_user_id == user_id).all()),
            "mv_thefts": serialize(self.db.query(mvTheft).filter(mvTheft.clerk_user_id == user_id).all()),
            "sos_reports": serialize(self.db.query(SOSReport).filter(SOSReport.clerk_user_id == user_id).all())
        }

    def register_lost_item(self, data: LostItemCreate) -> LostItem:
        return self.repository.save_fir(LostItem(**data.model_dump()))

    def register_cyber_crime(self, data: CyberCrimeCreate) -> cyberCrime:
        return self.repository.save_fir(cyberCrime(**data.model_dump()))

    def register_rape_case(self, data: RapeCaseCreate) -> rapecase:
        return self.repository.save_fir(rapecase(**data.model_dump()))

    def register_domestic_form(self, data: DomesticFormCreate) -> domesticForm:
        return self.repository.save_fir(domesticForm(**data.model_dump()))

    def register_theft_efir(self, data: TheftEfirCreate) -> theftEfir:
        return self.repository.save_fir(theftEfir(**data.model_dump()))

    def register_mv_theft(self, data: MVTheftCreate) -> mvTheft:
        return self.repository.save_fir(mvTheft(**data.model_dump()))

    def register_missing_person(self, data: MissingPersonCreate) -> missingPerson:
        return self.repository.save_fir(missingPerson(**data.model_dump()))
