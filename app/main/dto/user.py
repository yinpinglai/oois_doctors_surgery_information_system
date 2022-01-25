from flask_restx import Namespace, fields
from .appointment import AppointmentDto


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'name': fields.String(required=True, description='user name'),
        'employee_number': fields.String(required=True, description='user employee_number'),
        'position': fields.String(description='user position'),
        'appointments': fields.List(fields.Nested(AppointmentDto.appointment)),
        'public_id': fields.String(description='user Identifier'),
    })

