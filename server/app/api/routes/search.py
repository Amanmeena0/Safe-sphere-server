from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.api.dependencies import get_db
from typing import Optional

router = APIRouter()

@router.get("/search")
async def search(
    state_ut: Optional[str] = None,
    district: Optional[str] = None,
    year: Optional[int] = None,
    limit: int = Query(50, gt=0),
    db: Session = Depends(get_db)
):
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
    
    result = db.execute(text(query_str), params)
    return [dict(row) for row in result.mappings()]
