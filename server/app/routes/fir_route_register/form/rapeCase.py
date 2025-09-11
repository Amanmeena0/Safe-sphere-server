from flask import Blueprint, request, jsonify
from app.models import db, rapecase
from datetime import datetime
import os
import requests

rapecase_bp = Blueprint('rapecase', __name__)

@rapecase_bp.route('/rape_case', methods=['POST'])
def report_rape_case():
    data = request.json
    new_rape_case = rapecase(
        victim_name=data['victim_name'],
        age=data['age'],
        gender=data['gender'],
        incidentDetails=data['incidentDetails'],
        perpetrator_details=data['perpetrator_details'],
        location_of_incident=data['location_of_incident'],
        date_of_incident=data['date_of_incident'],
        time_of_incident=data['time_of_incident'],
        upload_documents=data['upload_documents'],
        informant_details=data['informant_details'],
        police_station=data['police_station'],
    )
    db.session.add(new_rape_case)
    db.session.commit()
    return jsonify({"message": "Rape case reported successfully"}), 201
