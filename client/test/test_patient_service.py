import unittest

from client.config import config_by_name
from client.model.patient import Patient
from client.service.auth_service import AuthService
from client.service.patient_service import PatientService

class TestPatientService(unittest.TestCase):

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

    @classmethod
    def tearDownClass(cls) -> None:
        config = config_by_name['test']
        auth_service = AuthService(config)
        is_success = auth_service.logout(cls.token)

        if is_success:
            cls.token = ''
            cls.headers = {}

    def test_get_patient_list(self):
        assert self.token is not None

        patient_service = PatientService(self.config, self.headers)
        patient_list = patient_service.get_patient_list()

        assert len(patient_list) > 0


    def test_get_patient(self):
        assert self.token is not None

        patient_service = PatientService(self.config, self.headers)
        patient_list = patient_service.get_patient_list()

        assert issubclass(type(patient_list[0]), Patient)
        patient_public_id = patient_list[0].public_id

        patient = patient_service.get_patient(patient_public_id)
        assert patient is not None
        assert issubclass(type(patient), Patient)
        assert patient.public_id == patient_public_id


if __name__ == '__main__':
    unittest.main()

