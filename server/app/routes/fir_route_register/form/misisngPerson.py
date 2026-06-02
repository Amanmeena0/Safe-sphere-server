from flask import Blueprint, request, jsonify
from app.models import db, missingPerson
from datetime import datetime
from app.utils.auth import verify_token
import os
import requests


missingPerson_bp = Blueprint('missingPerson', __name__)

@missingPerson_bp.route('/api/firs/missing_person', methods=['POST'])
@verify_token
def report_missing_person():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Convert date_time_last_seen to datetime object if it's a string
        date_time_last_seen = data['date_time_last_seen']
        if isinstance(date_time_last_seen, str):
            date_time_last_seen = datetime.fromisoformat(date_time_last_seen.replace('Z', '+00:00'))
            
        new_missing_person = missingPerson(
            user_auth_id=request.user_id,
            Fullname=data['name'],
            Numberofperson=int(data['number_of_person']),
            nickname=data['nick_name'],
            fathername=data['father_name'],
            relation=data['relation'],
            lastknownlocation=data['last_known_address'],
            gender=data['gender'],
            yearofbirth=int(data['year_of_birth']),
            agefrom=int(data['age_from']),
            ageto=int(data['age_to']),
            bodybuild=data['body_build'],
            complexion=data['complexion'],
            weight=float(data['weight']),
            height=float(data['height_range']),
            incidentReport=data['incident_report'],
            detailsLastseen=data['details_last_seen'],
            datetimelastseen=date_time_last_seen,
            complainant_name=data['complainant_name'],
            relationwithMissingperson=data['relation_with_missing_person'],
            complainant_address=data['complainant_address'],
            complainant_contact=data['complainant_contact'],
            alternate_contact=data['alternate_number'],
            emailaddress=data['email_address'],
            anyotherdetails=data['any_other_details'],
            policestation=data['police_station'],
            district=data['complainant_district'],
            upload_document=data.get('image', b''),  # Default to empty bytes if no image
        )
        db.session.add(new_missing_person)
        db.session.commit()
        return jsonify({"message": "Missing person reported successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
