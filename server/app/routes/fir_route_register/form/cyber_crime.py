from flask import Blueprint, request, jsonify
from app.models import db, cyberCrime
from datetime import datetime
from app.utils.auth import verify_token
import os

cyber_crime_bp = Blueprint('cyber_crime', __name__)

@cyber_crime_bp.route('/api/firs/cyber-crime/', methods=['POST'])
@verify_token
def register_cyber_crime():
    data = request.get_json()

    required_fields = ['incidentType', 'platefrom', 'dateOfIncident', 'reporterName',
                       'reporterContact', 'location', 'reporterAge',
                       'reporterGender', 'reporterRelation', 'policeStation', 'description'
                       ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400

    try:
        date_of_incident = datetime.strptime(data['dateOfIncident'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format for date of incident'}), 400

    new_cyber_crime = cyberCrime(
        user_auth_id=request.user_id,
        crimeCategory=data['incidentType'],
        platform = data['platefrom'],
        date_of_incident = data['dateOfIncident'],
        time = data.get('time'),
        IpAddress = data.get('ipAddress'),
        description=data['description'],
        digitalEvidence=data.get('digitalEvidence', ''),
        full_name=data['reporterName'],
        contact_number=data['reporterContact'],
        email=data.get('reporterEmail', ''),
        address = data['location'],
        age= data['reporterAge'],
        gender = data['reporterGender'],
        relation = data['reporterRelation'],
        policeStation = data['policeStation'],
    )

    db.session.add(new_cyber_crime)
    db.session.commit()

    return jsonify({
        'message': 'Cyber crime registered successfully',
        'cyber_crime_id': new_cyber_crime.id
    }), 201