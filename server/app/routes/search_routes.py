from flask import Blueprint, request, jsonify
from app.utils import execute_query

search_bp = Blueprint('search', __name__)

@search_bp.route("/search", methods=['GET'])
def search():
    state_ut = request.args.get('state_ut')
    district = request.args.get('district')
    year = request.args.get('year')
    limit = request.args.get('limit', 50, type=int)

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

    query = "SELECT * FROM crime_data"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += f" LIMIT {limit}"
    
    data = execute_query(query, params)
    return jsonify(data), 200



