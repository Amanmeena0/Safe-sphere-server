from flask import Blueprint, request, jsonify
from app.models import db, rapecase
from datetime import datetime
from app.utils.auth import verify_token
import os
import requests

rapecase_bp = Blueprint('rapecase', __name__)

@rapecase_bp.route('/api/firs/rape-case', methods=['POST'])
@verify_token
def report_rape_case():
    try:
        data = request.json
        
        # Convert date_of_incident to date object if it's a string
        date_of_incident = data['date_of_incident']
        if isinstance(date_of_incident, str):
            date_of_incident = datetime.strptime(date_of_incident, '%Y-%m-%d').date()

        new_rape_case = rapecase(
            user_auth_id=request.user_id,
            victim_name=data['victim_name'],
            age=data['age'],
            gender=data['gender'],
            incidentDetails=data['incidentDetails'],
            perpetratorDetails=data['perpetrator_details'],
            location_of_incident=data['location_of_incident'],
            date_of_incident=date_of_incident,
            time_of_incident=data['time_of_incident'],
            upload_document=data.get('upload_documents', ''),
            informant_details=data['informant_details'],
            police_station=data['police_station'],
        )
        db.session.add(new_rape_case)
        db.session.commit()
        return jsonify({"message": "Rape case reported successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
