from flask_restx import Namespace, fields
from .api import produce_api_response_structure
from .prescription import PrescriptionDto
from .appointment import AppointmentDto


class PatientDto:
    api = Namespace('patient', description='patient related operations')
    patient = api.model('patient', {
        'name': fields.String(required=True, description='patient name'),
        'address': fields.String(required=True, description='patient address'),
        'phone': fields.String(required=True, description='patient phone'),
        'public_id': fields.String(description='patient Identifier'),
        'prescriptions': fields.List(fields.Nested(PrescriptionDto.prescription)),
        'appointments': fields.List(fields.Nested(AppointmentDto.appointment)),
    })
    patient_list_api = api.model('patient_list_api', produce_api_response_structure(
        patient,
        is_list=True,
    ))
    patient_details_api = api.model('patient_details_api', produce_api_response_structure(
        patient,
    ))
    patient_changed_response = api.model('patient_changed_response', produce_api_response_structure(
        api.model('patient_successfully_changed_response', {
           'id': fields.String(description='patient Identifier'),
        }),
    ))
