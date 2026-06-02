from flask import Blueprint, request, jsonify
from app.models import db, User
from datetime import datetime
from app.utils.auth import verify_token
import os

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile/register', methods=['POST'])
@verify_token
def register_user():
    try:
        data = request.get_json()

        # authId is now securely extracted from the verified token
        auth_id = request.user_id
        
        required_fields = ['name', 'email', 'phone', 'address', 'aadharNumber', 'role', 'dateOfBirth', 'emergencyContact', 'emergencyContactPhone']

        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400

        existing_user = User.query.filter_by(auth_id=auth_id).first()
        if existing_user:
            return jsonify({'error': 'User already registered'}), 400

        existing_aadhar = User.query.filter_by(aadhar_number=data['aadharNumber']).first()
        if existing_aadhar:
            return jsonify({'error': 'Aadhar number already registered'}), 400

        if len(data['aadharNumber']) != 12 or not data['aadharNumber'].isdigit():
            return jsonify({'error': 'Invalid Aadhar number. Must be 12 digits'}), 400

        if data['role'] not in ['civilian', 'police']:
            return jsonify({'error': 'Invalid role'}), 400

        try:
            dob = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format for date of birth'}), 400

        new_user = User(
            auth_id=auth_id,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            aadhar_number=data['aadharNumber'],
            role=data['role'],
            date_of_birth=dob,
            emergency_contact_name=data['emergencyContact'],
            emergency_contact_phone=data['emergencyContactPhone'],
            registration_date=datetime.utcnow(),
            status='active'
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'User registered successfully',
            'user_id': new_user.id,
            'role': new_user.role
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500

@user_bp.route('/profile/check', methods=['GET'])
@verify_token
def check_user_profile():
    try:
        # Use the verified auth_id from the token
        auth_id = request.user_id
        user = User.query.filter_by(auth_id=auth_id).first()

        if user:
            return jsonify({
                'exists': True,
                'profile_completed': True,
                'role': user.role,
                'user_data': {
                    'name': user.name,
                    'email': user.email,
                    'phone': user.phone,
                    'role': user.role,
                    'registration_date': user.registration_date.isoformat() if user.registration_date else None
                }
            }), 200
        else:
            return jsonify({
                'exists': False,
                'profile_completed': False
            }), 200

    except Exception as e:
        return jsonify({'error': f'Failed to check profile: {str(e)}'}), 500

@user_bp.route('/profile/update', methods=['PUT'])
@verify_token
def update_user_profile():
    try:
        auth_id = request.user_id
        user = User.query.filter_by(auth_id=auth_id).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()

        allowed_fields = ['name', 'phone', 'address', 'emergency_contact_name', 'emergency_contact_phone']

        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'message': 'Profile updated successfully',
            'user_id': user.id
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Update failed: {str(e)}'}), 500
