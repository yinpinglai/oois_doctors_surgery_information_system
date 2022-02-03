import unittest
from datetime import datetime, timedelta

from client.config import config_by_name
from client.model.appointment import Appointment
from client.enum.appointment_type import AppointmentType
from client.enum.appointment_status import AppointmentStatus
from client.service.auth_service import AuthService
from client.service.patient_service import PatientService
from client.service.appointment_service import AppointmentService
from client.service.healthcare_professional_service import HealthcareProfessionalService

class TestAppointmentService(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.config = config_by_name['test']

    @classmethod
    def setUpClass(cls):
        config = config_by_name['test']
        auth_service = AuthService(config)
        is_success, token = auth_service.login(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )
        if is_success:
            cls.token = token
            cls.headers = {
                'Authorization': cls.token,
            }

        healthcare_professional_service = HealthcareProfessionalService(config, cls.headers)
        healthcare_professional_list = healthcare_professional_service.get_healthcare_professional_list()

        if len(healthcare_professional_list) == 0:
            cls.healthcare_professional = None
            return

        cls.healthcare_professional = healthcare_professional_list[0]

        patient_service = PatientService(config, cls.headers)
        patient_list = patient_service.get_patient_list()

        if len(patient_list) == 0:
            cls.patient = None
            return

        cls.patient = patient_list[0]


    @classmethod
    def tearDownClass(cls) -> None:
        config = config_by_name['test']
        auth_service = AuthService(config)
        is_success = auth_service.logout(cls.token)

        if is_success:
            cls.token = ''
            cls.headers = {}

    def test_make_an_appointment(self):
        assert self.token is not None
        assert self.healthcare_professional is not None
        assert self.patient is not None

        appointment_service = AppointmentService(self.config, self.headers)
        appointment = Appointment()
        appointment.type = AppointmentType.standard.value
        appointment.patient_id = self.patient.public_id
        appointment.healthcare_professional_id = self.healthcare_professional.public_id
        appointment.start_time = datetime.utcnow()
        appointment.end_time = appointment.start_time + timedelta(hours=1)

        result = appointment_service.make_an_appointment(appointment)
        assert result['id'] is not None

    def test_cancel_an_appointment(self):
        assert self.token is not None
        assert self.healthcare_professional is not None
        assert self.patient is not None

        appointment_service = AppointmentService(self.config, self.headers)
        appointment = Appointment()
        appointment.type = AppointmentType.standard.value
        appointment.patient_id = self.patient.public_id
        appointment.healthcare_professional_id = self.healthcare_professional.public_id
        appointment.start_time = datetime.utcnow()
        appointment.end_time = appointment.start_time + timedelta(hours=1)
        result = appointment_service.make_an_appointment(appointment)
        assert result['id'] is not None
        appointment.public_id = result['id']
        appointment.status = AppointmentStatus.cancelled.value

        result = appointment_service.cancel_an_appointment(appointment)
        assert result['id'] is not None

    def test_perform_consulting_service(self):
        assert self.token is not None
        assert self.healthcare_professional is not None
        assert self.patient is not None

        appointment_service = AppointmentService(self.config, self.headers)
        appointment = Appointment()
        appointment.type = AppointmentType.standard.value
        appointment.patient_id = self.patient.public_id
        appointment.healthcare_professional_id = self.healthcare_professional.public_id
        appointment.start_time = datetime.utcnow()
        appointment.end_time = appointment.start_time + timedelta(hours=1)
        result = appointment_service.make_an_appointment(appointment)
        assert result['id'] is not None
        appointment.public_id = result['id']

        result = appointment_service.perform_consulting_service(appointment)
        assert result['id'] is not None


    def test_get_appointment_list(self):
        assert self.token is not None

        appointment_service = AppointmentService(self.config, self.headers)
        appointment_list = appointment_service.get_appointment_list()

        assert len(appointment_list) > 0
        appointment = appointment_list[0]
        assert appointment.public_id is not None

    def test_get_appointment(self):
        assert self.token is not None

        appointment_service = AppointmentService(self.config, self.headers)
        appointment_list = appointment_service.get_appointment_list()

        assert len(appointment_list) > 0
        appointment = appointment_list[0]
        assert issubclass(type(appointment), Appointment)
        appointment_public_id = appointment.public_id
        appointment = appointment_service.get_appointment(appointment_public_id)

        assert appointment is not None
        assert appointment.public_id == appointment_public_id

