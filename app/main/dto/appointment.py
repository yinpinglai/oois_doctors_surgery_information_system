from flask_restx import Namespace, fields


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

