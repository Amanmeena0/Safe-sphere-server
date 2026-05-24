from app.models import db
from sqlalchemy import text

def execute_query(query, params=None):
    try:
        # Use SQLAlchemy session to execute the query
        # This allows the app to work with SQLite, MySQL, or any other DB configured
        
        # Handle parameter placeholder differences between MySQL (%s) and SQLite (?)
        if 'sqlite' in str(db.engine.url):
            query = query.replace('%s', '?')
        
        # In SQLAlchemy 1.4+, we use text() for raw SQL
        result = db.session.execute(text(query), params or ())
        
        # Convert results to list of dictionaries for JSON serialization
        if result.returns_rows:
            return [dict(row) for row in result.mappings()]
        return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
