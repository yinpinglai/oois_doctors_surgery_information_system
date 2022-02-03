import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    PORT = 5050
    SECRET_KEY = 'thisisthesecretkey'

    API_HOST = os.getenv('API_HOST', 'http://127.0.0.1')
    API_PORT = os.getenv('API_PORT', '5000')

    # Client Application Window Config
    TITLE = 'Doctors\' Surgery Client App'
    WIDTH = 800
    HEIGHT = 600

    # API config
    API_PREFIX = 'api'

    # Auth API
    AUTH_API_LOGIN_RESOURCE_URL = 'auth/login'
    AUTH_API_LOGOUT_RESOURCE_URL = 'auth/logout'
    AUTH_API_USER_INFO_URL = 'auth/user-info'

    # Patient API
    PATIENT_API_GET_PATIENT_LIST_RESOURCE_URL = 'patient'
    PATIENT_API_GET_PATIENT_RESOURCE_URL = 'patient'
    PATIENT_API_CREATE_OR_UPDATE_PATIENT_RESOURCE_URL = 'patient'

    # Healthcare Professional API
    HEALTHCARE_PROFESSIONAL_API_GET_HEALTHCARE_PROFESSIONAL_LIST_RESOURCE_URL = 'user/'
    HEALTHCARE_PROFESSIONAL_API_GET_HEALTHCARE_PROFESSIONAL_RESOURCE_URL = 'user'

    # Prescription API
    PRESCRIPTION_API_ISSUE_PRESCRIPTION_RESOURCE_URL = 'prescription/'
    PRESCRIPTION_API_REQUEST_AN_REPEATABLE_PRESCRIPTION_RESOURCE_URL = 'prescription'

    # Appointment API
    APPOINTMENT_API_GET_APPOINTMENT_LIST_RESOURCE_URL = 'appointment'
    APPOINTMENT_API_GET_APPOINTMENT_DETAILS_RESOURCE_URL = 'appointment'
    APPOINTMENT_API_MAKE_AN_APPOINTMENT_RESOURCE_URL = 'appointment/'
    APPOINTMENT_API_CANCEL_AN_APPOINTMENT_RESOURCE_URL = 'appointment'
    APPOINTMENT_API_UPDATE_STATUS_OF_AN_APPOINTMENT_RESOURCE_URL = 'appointment'
    APPOINTMENT_API_GET_NEXT_AVAILABLE_TIMESLOT_RESOURCE_URL = 'appointment'



class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig,
)

