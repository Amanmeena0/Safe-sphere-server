from sqlalchemy.orm import Session
from app.repositories.crime_repository import CrimeRepository
from typing import Optional, List, Dict

class CrimeService:
    def __init__(self, db: Session):
        self.repository = CrimeRepository(db)

    def search_crime(
        self,
        state_ut: Optional[str] = None,
        district: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict]:
        return self.repository.search_crime_data(
            state_ut=state_ut,
            district=district,
            year=year,
            limit=limit
        )
