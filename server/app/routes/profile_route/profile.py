from flask import Flask, jsonify, Blueprint, request
from app.models import db, User
from sqlalchemy.exc import SQLAlchemyError

# Create a Blueprint for profile routes
profile_bp = Blueprint('profile', __name__)

@profile_bp.route("/api/profile/<auth_id>", methods=['GET'])
def get_profile(auth_id):
    try:
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

# ✅ New DELETE endpoint
@profile_bp.route("/api/profile/<auth_id>", methods=['DELETE'])
def delete_profile(auth_id):
    try:
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
