import re
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from models import User

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    return len(phone) == 10 and phone.isdigit()

def validate_aadhaar(aadhaar):
    return len(aadhaar) == 12 and aadhaar.isdigit()

def admin_required(f):
    """Decorator to require admin role for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        if not user or user.role != 'admin':
            return jsonify({'message': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Get current user from JWT token"""
    current_user_id = int(get_jwt_identity())
    return User.query.get(current_user_id)
