from flask import Blueprint, request, jsonify
from app.models import db, LostItem
from datetime import datetime
from app.utils.auth import verify_token
import os
import requests

lost_item_bp = Blueprint('lost_item', __name__)

@lost_item_bp.route('/api/firs/lost-item', methods=['POST'])
@verify_token
def register_lost_item():
    data = request.get_json()

    required_fields = ['itemName', 'brandname', 'model', 'placeofloss', 'lossdatetime', 'ownerName', 'contactNumber', 'address', 'documentType', 'policeStation', 'district']

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400

    try:
        date_found = datetime.strptime(data['dateFound'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format for date found'}), 400

    new_lost_item = LostItem(
        user_auth_id=request.user_id,
        item_name=data['itemName'],
        brand=data['brandname'],
        model=data['model'],
        placeofloss=data['placeofloss'],
        loss_datetime=data['lossdatetime'],
        owner_name=data['ownerName'],
        contact_number=data['contactNumber'],
        address=data['address'],
        document_type=data['documentType'],
        police_station=data['policeStation'],
        district=data['district'],
    )

    db.session.add(new_lost_item)
    db.session.commit()

    return jsonify({
        'message': 'Lost item registered successfully',
        'lost_item_id': new_lost_item.id
    }), 201