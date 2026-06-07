from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List, Dict

class CrimeRepository:
    def __init__(self, db: Session):
        self.db = db

    def search_crime_data(
        self,
        state_ut: Optional[str] = None,
        district: Optional[str] = None,
        year: Optional[int] = None,
        limit: int = 50
    ) -> List[Dict]:
        conditions = []
        params = {}

        if state_ut:
            conditions.append("state_ut ILIKE :state_ut")
            params['state_ut'] = f'%{state_ut}%'
        
        if district:
            conditions.append("district ILIKE :district")
            params['district'] = f'%{district}%'
        
        if year:
            conditions.append("year = :year")
            params['year'] = year

        query_str = "SELECT * FROM crime_data"
        if conditions:
            query_str += " WHERE " + " AND ".join(conditions)
        
        query_str += f" LIMIT {limit}"
        
        result = self.db.execute(text(query_str), params)
        return [dict(row) for row in result.mappings()]
