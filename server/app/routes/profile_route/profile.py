from flask import jsonify, Blueprint, request
from app.models import db, User, cyberCrime, theftEfir, LostItem, missingPerson, domesticForm, rapecase, mvTheft
from sqlalchemy.exc import SQLAlchemyError
from app.utils.auth import verify_token

# Create a Blueprint for profile routes
profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/api/profile", methods=['GET'])
@verify_token
def get_profile():
    try:
        auth_id = request.user_id
        user = User.query.filter_by(auth_id=auth_id).first()
        
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_data = {
            "id": user.id,
            "auth_id": user.auth_id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "address": user.address,
            "aadhar_number": user.aadhar_number,
            "role": user.role,
            "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else None,
            "emergency_contact_name": user.emergency_contact_name,
            "emergency_contact_phone": user.emergency_contact_phone,
            "registration_date": user.registration_date.isoformat() if user.registration_date else None,
            "updated_at": user.updated_at.isoformat() if user.updated_at else None,
            "status": user.status
        }

        return jsonify(user_data), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error", "details": str(e)}), 500

@profile_bp.route("/api/profile/my-firs", methods=['GET'])
@verify_token
def get_my_firs():
    """
    Fetch all types of reports submitted by the authenticated citizen.
    """
    try:
        auth_id = request.user_id
        
        # Helper to serialize model data
        def serialize(items):
            return [{c.name: getattr(item, c.name) for c in item.__table__.columns} for item in items]

        data = {
            "cyber_crimes": serialize(cyberCrime.query.filter_by(user_auth_id=auth_id).all()),
            "theft_efirs": serialize(theftEfir.query.filter_by(user_auth_id=auth_id).all()),
            "lost_items": serialize(LostItem.query.filter_by(user_auth_id=auth_id).all()),
            "missing_persons": serialize(missingPerson.query.filter_by(user_auth_id=auth_id).all()),
            "domestic_forms": serialize(domesticForm.query.filter_by(user_auth_id=auth_id).all()),
            "rape_cases": serialize(rapecase.query.filter_by(user_auth_id=auth_id).all()),
            "mv_thefts": serialize(mvTheft.query.filter_by(user_auth_id=auth_id).all())
        }

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch reports", "details": str(e)}), 500

@profile_bp.route("/api/profile", methods=['DELETE'])
@verify_token
def delete_profile():
    try:
        auth_id = request.user_id
        user = User.query.filter_by(auth_id=auth_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User profile deleted successfully."}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": "Database error occurred", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500
