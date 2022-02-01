from flask_restx import Namespace, fields
from .api import produce_api_response_structure


class PrescriptionDto:
    api = Namespace('prescription', description='prescription related operations')
    prescription = api.model('prescription', {
        'type': fields.String(required=True, description='prescription type'),
        'patient_id': fields.String(required=True, description='prescription for patient'),
        'doctor_id': fields.String(required=True, description='prescription issued by doctor'),
        'quantity': fields.Integer(required=True, description='prescription quantity'),
        'dosage': fields.String(required=True, description='prescription dosage'),
        'public_id': fields.String(description='prescription Identifier'),
        'created_on': fields.DateTime(description='prescription created time'),
    })
    prescription_details = api.model('prescription_details', {
        'type': fields.String(description='prescription type'),
        'quantity': fields.Integer(description='prescription quantity'),
        'dosage': fields.String(description='prescription dosage'),
    })
    prescription_list_api = api.model('prescription_list_api', produce_api_response_structure(
        prescription,
        is_list=True,
    ))
    prescription_details_api = api.model('prescription_details_api', produce_api_response_structure(
        prescription_details,
    ))
    prescription_changed_response = api.model('prescription_changed_response', produce_api_response_structure(
        api.model('prescription_successfully_changed_response', {
           'id': fields.String(description='prescription Identifier'),
        }),
    ))

