from flask_restx import Namespace, fields


class PatientDto:
	api = Namespace('patient', description='patient related operations')
	patient = api.model('patient', {
		'name': fields.String(required=True, description='patient name'),
		'address': fields.String(required=True, description='patient address'),
		'phone': fields.String(required=True, description='patient phone'),
		'public_id': fields.String(description='patient Identifier'),
	})


class PrescriptionDto:
	api = Namespace('prescription', description='prescription related operations')
	prescription = api.model('prescription', {
		'type': fields.String(required=True, description='prescription type'),
		'patient_id': fields.String(required=True, description='prescription for patient'),
		'doctor_id': fields.String(required=True, description='prescription issued by doctor'),
		'quantity': fields.Integer(required=True, description='prescription quantity'),
		'dosage': fields.String(required=True, description='prescription dosage'),
		'public_id': fields.String(description='prescription Identifier')
	})
	prescription_details = api.model('prescription_details', {
		'type': fields.String(description='prescription type'),
		'quantity': fields.Integer(description='prescription quantity'),
		'dosage': fields.String(description='prescription dosage'),
	})


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'name': fields.String(required=True, description='user name'),
        'employee_number': fields.String(required=True, description='user employee_number'),
        'position': fields.String(description='user position'),
        'public_id': fields.String(description='user Identifier'),
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })
