from flask_restx import Namespace, fields
from .appointment import AppointmentDto
from .api import produce_api_response_structure


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
    user_list_api = api.model('user_list_api', produce_api_response_structure(
        user,
        is_list=True,
    ))
    user_details_api = api.model('user_details_api', produce_api_response_structure(
        user,
    ))
    user_changed_response = api.model('user_changed_response', produce_api_response_structure(
        api.model('user_successfully_changed_response', {
           'id': fields.String(description='user Identifier'),
           'Authorization': fields.String(descritpion='user access token'),
        }),
    ))

