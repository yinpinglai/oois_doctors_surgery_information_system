from flask import request
from flask_restx import Resource, reqparse

from app.main.dto.appointment import AppointmentDto
from app.main.util.decorator import token_required, receptionist_token_required
from ..service.appointment_service import delete_an_appointment, save_new_appointment, get_all_appointments, get_an_appointment, update_an_appointment, delete_an_appointment
from typing import Dict, Tuple

api = AppointmentDto.api
_appointment = AppointmentDto.appointment
_appointment_details = AppointmentDto.appointment_details
_appointment_list_api = AppointmentDto.appointment_list_api
_appointment_details_api = AppointmentDto.appointment_details_api
_appointment_changed_response = AppointmentDto.appointment_changed_response


@api.route('/')
class AppointmentList(Resource):

    @token_required
    @api.doc(
        'Gets the list of appointments',
        params={
            'start_time': 'The start time used for filtering the list of appointments.',
            'end_time': 'The end time used for filtering the list of appointments.',
            'sort_by': 'The key used for sorting the list of appointments.',
            'sort_order': 'The sorting order while sorting the list of appointments.',
        }
    )
    @api.marshal_list_with(_appointment_list_api)
    def get(self):
        ''' List all booked appointments '''
        parser = reqparse.RequestParser()
        parser.add_argument('start_time', type=str, help='The start time used for filtering the list of appointments.')
        parser.add_argument('end_time', type=str, help='The end time used for filtering the list of appointments.')
        parser.add_argument('sort_by', type=str, help='The key used for sorting the list of appointments.')
        parser.add_argument('sort_order', type=str, help='The sorting order while sorting the list of appointments.')
        params = parser.parse_args()
        return get_all_appointments(params)

    @receptionist_token_required
    @api.expect(_appointment, validate=True)
    @api.response(201, 'Appointment successfully booked.', _appointment_changed_response)
    @api.doc(
        'Books a new appointment',
        responses={
            409: 'Request contains a conflit and cannot be accepted.',

        },
    )
    def post(self) -> Tuple[Dict[str, str], int]:
        ''' Books a new appointment '''
        data = request.json
        return save_new_appointment(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The appointment identifier')
@api.response(404, 'Appointment not found.')
class Appointment(Resource):

    @token_required
    @api.doc('Gets an appointment')
    @api.marshal_with(_appointment_details_api)
    def get(self, public_id):
        ''' Gets an appointment given its identifier '''
        appointment = get_an_appointment(public_id)
        if not appointment:
            api.abort(404)
        else:
            return appointment

    @receptionist_token_required
    @api.expect(_appointment_details, validate=True)
    @api.response(201, 'Appointment successfully updated.', _appointment_changed_response)
    @api.doc(
        'Updates an appointment',
        responses={
            409: 'Request contains a conflit and cannot be accepted.',
        },
    )
    def put(self, public_id):
        ''' Updates an appointment given its identifier '''
        data = request.json
        return update_an_appointment(public_id, data)

    @receptionist_token_required
    @api.response(200, 'Appointment record successfully deleted.', _appointment_changed_response)
    @api.doc('Deletes an appointment')
    def delete(self, public_id):
        ''' Deletes an appointment given its identifier '''
        return delete_an_appointment(public_id)

