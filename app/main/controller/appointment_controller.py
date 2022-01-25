from flask import request
from flask_restx import Resource

from app.main.dto.appointment import AppointmentDto
from app.main.util.decorator import token_required, receptionist_token_required
from ..service.appointment_service import delete_an_appointment, save_new_appointment, get_all_appointments, get_an_appointment, update_an_appointment, delete_an_appointment
from typing import Dict, Tuple

api = AppointmentDto.api
_appointment = AppointmentDto.appointment
_appointment_details = AppointmentDto.appointment_details


@api.route('/')
class AppointmentList(Resource):

    @token_required
    @api.doc('list_of_booked_appointments')
    @api.marshal_list_with(_appointment, envelope='data')
    def get(self):
        ''' List all booked appointments '''
        return get_all_appointments()

    @receptionist_token_required
    @api.expect(_appointment, validate=True)
    @api.response(201, 'Appointment successfully booked.')
    @api.doc('book a new appointment')
    def post(self) -> Tuple[Dict[str, str], int]:
        ''' Books a new appointment '''
        data = request.json
        return save_new_appointment(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The appointment identifier')
@api.response(404, 'Appointment not found.')
class Appointment(Resource):

    @token_required
    @api.doc('get an appointment')
    @api.marshal_with(_appointment_details)
    def get(self, public_id):
        ''' Gets an appointment given its identifier '''
        appointment = get_an_appointment(public_id)
        if not appointment:
            api.abort(404)
        else:
            return appointment

    @receptionist_token_required
    @api.expect(_appointment_details, validate=True)
    @api.doc('update an appointment')
    def put(self, public_id):
        ''' Updates an appointment given its identifier '''
        data = request.json
        return update_an_appointment(public_id, data)

    @receptionist_token_required
    @api.doc('delete an appointment')
    def delete(self, public_id):
        ''' Deletes an appointment given its identifier '''
        return delete_an_appointment(public_id)

