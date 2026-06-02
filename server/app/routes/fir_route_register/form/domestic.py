from flask import Blueprint, request, jsonify
from app.models import db, domesticForm
from app.utils.auth import verify_token
import os
from datetime import datetime

domestic_bp = Blueprint('domestic', __name__)
@domestic_bp.route('/api/firs/domestic/', methods=['POST'])
@verify_token
def register_domestic():
    data = request.get_json()

    required_fields = []

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400

    try:
        date_of_incident = datetime.strptime(data['dateOfIncident'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format for date of incident'}), 400

    new_domestic = domesticForm(
        user_auth_id=request.user_id,
        registeration_type = data['registerationType'],
        reporter_name = data['reporterName'],
        reporter_age = data['reporterAge'],
        reporter_gender = data['reporterGender'],
        reporter_contact = data['reporterContact'],
        reporter_Emailaddress = data['reporterEmailAddress'],
        reporter_native_place = data['reporterNativePlace'],
        employer_name = data['employerName'],
        employer_contact = data['employerContact'],
        employer_relations = data['employerrelations'],
        employer_address = data['employerAddress'],
        documentation = data['documentation'],
        duration_of_stay = data['durationOfStay'],
    )

    db.session.add(new_domestic)
    db.session.commit()

    return jsonify({'message': 'Domestic FIR registered successfully'}), 201
