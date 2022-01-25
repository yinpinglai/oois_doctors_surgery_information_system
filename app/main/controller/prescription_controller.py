from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required, doctor_token_required
from ..util.dto import PrescriptionDto
from ..service.prescription_service import save_new_prescription, get_all_prescritpions, get_a_prescription, update_a_prescription
from typing import Dict, Tuple

api = PrescriptionDto.api
_prescription = PrescriptionDto.prescription
_prescription_details = PrescriptionDto.prescription_details


@api.route('/')
class PrescriptionList(Resource):
	@api.doc('list_of_issued_prescriptions')
	@token_required
	@api.marshal_list_with(_prescription, envelope='data')
	def get(self):
		"""List all issued prescriptions"""
		return get_all_prescritpions()

	@doctor_token_required
	@api.expect(_prescription, validate=True)
	@api.response(201, 'Prescription successfully issued.')
	@api.doc('issue a new prescription by a doctor for a patient')
	def post(self) -> Tuple[Dict[str, str], int]:
		"""Issues a new prescription by a doctor for a patient"""
		data = request.json
		return save_new_prescription(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'The Prescription identifier')
@api.response(404, 'Prescription not found.')
class Prescription(Resource):
	@api.doc('get a prescription')
	@token_required
	@api.marshal_with(_prescription)
	def get(self, public_id):
		"""Gets a prescription given its identifier"""
		prescription = get_a_prescription(public_id)
		if not prescription:
			api.abort(404)
		else:
			return prescription

	@api.expect(_prescription_details, validate=True)
	@api.response(201, 'Prescription successfully updated.')
	@api.doc('update a prescription record by a doctor for a patient')
	@doctor_token_required
	def put(self, public_id):
		"""Updates a prescription by a doctor for a patient given its identifier"""
		data = request.json
		return update_a_prescription(public_id, data)

