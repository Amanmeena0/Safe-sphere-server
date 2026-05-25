from app.models import db
from sqlalchemy import text

def execute_query(query, params=None):
    try:
        # Use SQLAlchemy session to execute the query with named parameters
        # In SQLAlchemy 1.4+, we use text() for raw SQL
        result = db.session.execute(text(query), params or {})
        
        # Convert results to list of dictionaries for JSON serialization
        if result.returns_rows:
            return [dict(row) for row in result.mappings()]
        return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
