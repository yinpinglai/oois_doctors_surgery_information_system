from flask import request
from flask_restx import Resource

from app.main.dto.patient import PatientDto
from app.main.util.decorator import token_required, receptionist_token_required
from ..service.patient_service import save_new_patient, get_all_patients, get_a_patient
from typing import Dict, Tuple

api = PatientDto.api
_patient = PatientDto.patient


@api.route('/')
class PatientList(Resource):

    @token_required
    @api.doc('list_of_registered_patients')
    @api.marshal_list_with(_patient, envelope='data')
    def get(self):
        ''' List all registered patients'''
        return get_all_patients()

    @receptionist_token_required
    @api.expect(_patient, validate=True)
    @api.response(201, 'Patient successfully created.')
    @api.doc('create a new patient')
    def post(self) -> Tuple[Dict[str, str], int]:
        ''' Creates a new patient '''
        data = request.json
        return save_new_patient(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The Patient identifier')
@api.response(404, 'Patient not found.')
class Patient(Resource):
    @token_required
    @api.doc('get a patient')
    @api.marshal_with(_patient)
    def get(self, public_id):
        ''' Get a patient given its identifier '''
        patient = get_a_patient(public_id)
        if not patient:
            api.abort(404)
        else:
            return patient

