from flask_restx import Api
from flask import Blueprint

from .main.controller.patient_controller import api as patient_ns
from .main.controller.prescription_controller import api as prescription_ns
from .main.controller.appointment_controller import api as appointment_ns
from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns

blueprint = Blueprint('api', __name__, url_prefix='/api')
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='DOCTOR SURGERY SYSTEM API',
    version='1.0',
    description='a restful API service',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(patient_ns, path='/patient')
api.add_namespace(prescription_ns, path='/prescription')
api.add_namespace(appointment_ns, path='/appointment')
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
