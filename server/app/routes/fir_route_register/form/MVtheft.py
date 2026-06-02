from flask import Blueprint, request, jsonify
from app.models import db, mvTheft
from datetime import datetime
from app.utils.auth import verify_token
import os
import requests

mvtheft_bp = Blueprint('mvtheft', __name__)

@mvtheft_bp.route('/api/firs/mv-theft', methods=['POST'])
@verify_token
def report_mv_theft():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Convert date_of_theft to date object if it's a string
        date_of_theft = data['date_of_theft']
        if isinstance(date_of_theft, str):
            date_of_theft = datetime.strptime(date_of_theft, '%Y-%m-%d').date()
            
        new_mv_theft = mvTheft(
            user_auth_id=request.user_id,
            vehicleDetails=data['vehicle_details'],
            owner_details=data['owner_details'],
            date_of_theft=date_of_theft,
            timeoftheft=data['time_of_theft'],
            location_of_theft=data['location_of_theft'],
            previous_fir_details=data['previous_fir_details'],
            upload_document=data.get('upload_documents', b''),  # Default to empty bytes if no document
            police_station=data['police_station'],
        )
        db.session.add(new_mv_theft)
        db.session.commit()
        return jsonify({"message": "Motor vehicle theft reported successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
