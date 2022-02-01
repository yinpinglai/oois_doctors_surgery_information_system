from flask import request
from flask_restx import Resource

from app.main.dto.patient import PrescriptionDto
from app.main.util.decorator import token_required, doctor_token_required
from ..service.prescription_service import save_new_prescription, get_all_prescritpions, get_a_prescription, update_a_prescription
from typing import Dict, Tuple

api = PrescriptionDto.api
_prescription = PrescriptionDto.prescription
_prescription_details = PrescriptionDto.prescription_details
_prescription_list_api = PrescriptionDto.prescription_list_api
_prescription_details_api = PrescriptionDto.prescription_details_api
_prescription_changed_response = PrescriptionDto.prescription_changed_response


@api.route('/')
class PrescriptionList(Resource):

    @token_required
    @api.doc('Gets the list of prescription')
    @api.marshal_list_with(_prescription_list_api)
    def get(self):
        ''' List all issued prescriptions '''
        return get_all_prescritpions()

    @doctor_token_required
    @api.expect(_prescription, validate=True)
    @api.response(201, 'Prescription successfully issued.', _prescription_changed_response)
    @api.doc(
        'Issues a new prescription by a doctor for a patient',
        responses={
            404: 'Prescription record not found. Please create a new record first.',
            409: 'Unsupported prescription type: {type} found.'
        },
    )
    def post(self) -> Tuple[Dict[str, str], int]:
        ''' Issues a new prescription by a doctor for a patient '''
        data = request.json
        return save_new_prescription(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The Prescription identifier')
@api.response(404, 'Prescription not found.')
class Prescription(Resource):

    @token_required
    @api.doc('Gets a prescription')
    @api.marshal_with(_prescription_details_api)
    def get(self, public_id):
        ''' Gets a prescription given its identifier '''
        prescription = get_a_prescription(public_id)
        if not prescription:
            api.abort(404)
        else:
            return prescription

    @doctor_token_required
    @api.expect(_prescription_details, validate=True)
    @api.response(201, 'Prescription successfully updated.', _prescription_changed_response)
    @api.doc(
        'Updates a prescription record by a doctor for a patient',
        responses={
            404: 'Prescription record not found. Please create a new record first.',
            409: 'Unsupported prescription type: {type} found.',
        },
    )
    def put(self, public_id):
        ''' Updates a prescription by a doctor for a patient given its identifier '''
        data = request.json
        return update_a_prescription(public_id, data)

