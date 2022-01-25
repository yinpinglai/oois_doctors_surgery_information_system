from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth
from app.main.enum.position_type import PositionType
from typing import Callable


def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated


def admin_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        admin = token.get('admin')
        if not admin:
            response_object = {
                'status': 'fail',
                'message': 'admin token required'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

def receptionist_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        position = token.get('position')
        if position != PositionType.receptionist.value:
            response_object = {
                'status': 'fail',
                'message': 'receptionist token required'
            }
            return response_object, 401
        
        return f(*args, **kwargs)
    return decorated

def healthcare_professional_token_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        position = token.get('position')
        if position != PositionType.doctor.value and position != PositionType.nurse.value:
            response_object = {
                'status': 'fail',
                'message': 'healthcare professional token required'
            }
            return response_object, 401
        
        return f(*args, **kwargs)
    return decorated
