from flask_restx import Namespace, fields
from .api import produce_api_response_structure


class AppointmentDto:
    api = Namespace('appointment', description='appointment related operations')
    appointment = api.model('appointment', {
        'type': fields.String(required=True, description='appointment type'),
		'patient_id': fields.String(required=True, description='appointment booked for patient'),
		'healthcare_professional_id': fields.String(required=True, description='appointment assigned to healthcare professional'),
		'start_time': fields.DateTime(required=True, description='appointment start time'),
		'end_time': fields.DateTime(required=True, description='appointment end time'),
		'public_id': fields.String(description='appointment Identifier'),
    })
    appointment_details = api.model('appointment_details', {
        'type': fields.String(required=True, description='appointment type'),
        'healthcare_professional_id': fields.String(required=True, description='appointment assigned to healthcare professional'),
		'start_time': fields.DateTime(required=True, description='appointment start time'),
		'end_time': fields.DateTime(required=True, description='appointment end time'),
    })
    appointment_list_api = api.model('appointment_list_api', produce_api_response_structure(
        appointment,
        is_list=True,
    ))
    appointment_details_api = api.model('appointment_details_api', produce_api_response_structure(
        appointment,
    ))
    appointment_changed_response = api.model('appointment_changed_response', produce_api_response_structure(
        api.model('appointment_successfully_changed_response', {
           'id': fields.String(description='appointment Identifier'),
        }),
    ))

