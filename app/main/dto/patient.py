from flask_restx import Namespace, fields
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

