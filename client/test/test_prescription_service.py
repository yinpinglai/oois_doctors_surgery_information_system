import unittest

from client.config import config_by_name
from client.model.patient import Patient
from client.model.doctor import Doctor
from client.model.prescription import Prescription
from client.enum.prescription_type import PrescriptionType
from client.service.auth_service import AuthService
from client.service.patient_service import PatientService
from client.service.prescription_service import PrescriptionService

class TestPrescriptionService(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.config = config_by_name['test']

    @classmethod
    def setUpClass(cls):
        config = config_by_name['test']
        auth_service = AuthService(config)
        is_success, token = auth_service.login(
            email='kenny.chan@gmail.com',
            password='P@ssw0rd',
        )
        if is_success:
            cls.token = token
            cls.headers = {
                'Authorization': cls.token,
            }

    @classmethod
    def tearDownClass(cls) -> None:
        config = config_by_name['test']
        auth_service = AuthService(config)
        is_success = auth_service.logout(cls.token)

        if is_success:
            cls.token = ''
            cls.headers = {}

    def test_issue_prescription(self):
        auth_service = AuthService(self.config)

        doctor = auth_service.get_user_info(self.token)
        assert issubclass(type(doctor), Doctor)

        patient_service = PatientService(self.config, self.headers)
        patient_list = patient_service.get_patient_list()
        assert len(patient_list) > 0

        patient_public_id = patient_list[0].public_id
        patient = patient_service.get_patient(patient_public_id)

        prescription = Prescription()
        prescription.type = PrescriptionType.standard.value
        prescription.doctor_id = doctor.public_id
        prescription.patient_id = patient.public_id
        prescription.quantity = 1
        prescription.dosage = 'Take one per four hours'

        prescription_service = PrescriptionService(self.config, self.headers)
        result = prescription_service.issue_prescription(prescription)

        assert result['id'] is not None


    def test_request_an_repeatable_prescription(self):
        config = config_by_name['test']
        auth_service = AuthService(config)

        doctor = auth_service.get_user_info(self.token)
        assert issubclass(type(doctor), Doctor)

        patient_service = PatientService(self.config, self.headers)
        patient_list = patient_service.get_patient_list()
        assert len(patient_list) > 0

        patient_public_id = patient_list[0].public_id
        patient = patient_service.get_patient(patient_public_id)

        assert len(patient.prescriptions) > 0
        prescription = patient.prescriptions[0]
        prescription.type = PrescriptionType.repeatable.value

        prescription_service = PrescriptionService(config, self.headers)
        result = prescription_service.request_an_repeatable_prescription(prescription)

        assert result['id'] is not None

