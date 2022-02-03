from flask_restx import Namespace, fields
from .api import produce_api_response_structure


class AppointmentDto:
    api = Namespace('appointment', description='appointment related operations')
    appointment_patient = api.model('appointment_patient', {
        'name': fields.String(description='patient name'),
        'address': fields.String(description='patient address'),
        'phone': fields.String(description='patient phone'),
        'public_id': fields.String(description='patient Identifier'),
    })
    appointment_healthcare_professional = api.model('appointment_healthcare_professional', {
        'name': fields.String(description='user name'),
        'employee_number': fields.String(description='user employee_number'),
        'position': fields.String(description='user position'),
        'public_id': fields.String(description='user Identifier'),
    })
    appointment = api.model('appointment', {
        'type': fields.String(required=True, description='appointment type'),
        'status': fields.Integer(required=True, description='appointment status'),
		'patient_id': fields.String(required=True, description='appointment booked for patient'),
		'healthcare_professional_id': fields.String(required=True, description='appointment assigned to healthcare professional'),
		'start_time': fields.DateTime(required=True, description='appointment start time'),
		'end_time': fields.DateTime(required=True, description='appointment end time'),
		'public_id': fields.String(description='appointment Identifier'),
        'patient': fields.Nested(appointment_patient),
        'healthcare_professional': fields.Nested(appointment_healthcare_professional),
    })
    appointment_details = api.model('appointment_details', {
        'type': fields.String(description='appointment type'),
        'status': fields.Integer(description='appointment status'),
        'healthcare_professional_id': fields.String(description='appointment assigned to healthcare professional'),
		'start_time': fields.DateTime(description='appointment start time'),
		'end_time': fields.DateTime(description='appointment end time'),
        'patient': fields.Nested(appointment_patient),
        'healthcare_professional': fields.Nested(appointment_healthcare_professional),
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

