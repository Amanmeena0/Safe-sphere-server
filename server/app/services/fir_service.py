from sqlalchemy.orm import Session
from app.repositories.fir_repository import FIRRepository
from app.schemas.fir import (
    LostItemCreate, CyberCrimeCreate, RapeCaseCreate, DomesticFormCreate,
    TheftEfirCreate, MVTheftCreate, MissingPersonCreate
)
from app.models.models import (
    LostItem, cyberCrime, rapecase, domesticForm, theftEfir, mvTheft, missingPerson
)

class FIRService:
    def __init__(self, db: Session):
        self.repository = FIRRepository(db)

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
