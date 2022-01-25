from flask_restx import Namespace, fields


class PrescriptionDto:
	api = Namespace('prescription', description='prescription related operations')
	prescription = api.model('prescription', {
		'type': fields.String(required=True, description='prescription type'),
		'patient_id': fields.String(required=True, description='prescription for patient'),
		'doctor_id': fields.String(required=True, description='prescription issued by doctor'),
		'quantity': fields.Integer(required=True, description='prescription quantity'),
		'dosage': fields.String(required=True, description='prescription dosage'),
		'public_id': fields.String(description='prescription Identifier'),
	})
	prescription_details = api.model('prescription_details', {
		'type': fields.String(description='prescription type'),
		'quantity': fields.Integer(description='prescription quantity'),
		'dosage': fields.String(description='prescription dosage'),
	})

