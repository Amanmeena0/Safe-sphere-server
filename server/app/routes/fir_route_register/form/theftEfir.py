from flask import Blueprint, request, jsonify
from app.models import db, theftEfir
from datetime import datetime
from app.utils.auth import verify_token
import os
import requests

theft_bp = Blueprint('theft', __name__)

@theft_bp.route('/theft', methods=['POST'])
@verify_token
def report_theft():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Convert date_of_theft to date object if it's a string
        date_of_theft = data['date_of_theft']
        if isinstance(date_of_theft, str):
            date_of_theft = datetime.strptime(date_of_theft, '%Y-%m-%d').date()
            
        new_theft = theftEfir(
            user_auth_id=request.user_id,
            incident_description=data['incident_description'],
            date_of_theft=date_of_theft,
            financial_impact=data.get('financial_impact', ''),  # Optional field
            witness_information=data.get('witness_information', ''),  # Optional field
            complainant_details=data.get('complainant_details', ''),  # Optional field
            upload_document=data.get('upload_documents', b''),  # Default to empty bytes if no document
            police_station=data['police_station'],
        )
        db.session.add(new_theft)
        db.session.commit()
        return jsonify({"message": "Theft reported successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except ValueError as e:
        return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500
