from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models.models import (
    LostItem, cyberCrime, rapecase, domesticForm, theftEfir, mvTheft, missingPerson
)
from typing import Type, TypeVar, Union

T_FIR = TypeVar("T_FIR", bound=Union[
    LostItem, cyberCrime, rapecase, domesticForm, theftEfir, mvTheft, missingPerson
])

class FIRRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_fir(self, fir_obj: T_FIR) -> T_FIR:
        self.db.add(fir_obj)
        self.db.commit()
        self.db.refresh(fir_obj)
        return fir_obj
