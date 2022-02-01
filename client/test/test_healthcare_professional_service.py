import unittest

from client.config import config_by_name
from client.model.healthcare_professional import HealthcareProfessional
from client.service.auth_service import AuthService
from client.service.healthcare_professional_service import HealthcareProfessionalService

class TestHealthcareProfessionalService(unittest.TestCase):

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

    def test_get_healthcare_professional_list(self):
        assert self.token is not None

        healthcare_professional_service = HealthcareProfessionalService(self.config, self.headers)
        healthcare_professional_list = healthcare_professional_service.get_healthcare_professional_list()

        assert len(healthcare_professional_list) > 0


    def test_get_healthcare_professional(self):
        assert self.token is not None

        healthcare_professional_service = HealthcareProfessionalService(self.config, self.headers)
        healthcare_professional_list = healthcare_professional_service.get_healthcare_professional_list()

        assert issubclass(type(healthcare_professional_list[0]), HealthcareProfessional)
        healthcare_professional_public_id = healthcare_professional_list[0].public_id

        healthcare_professional = healthcare_professional_service.get_healthcare_professional(healthcare_professional_public_id)
        assert healthcare_professional is not None
        assert issubclass(type(healthcare_professional), HealthcareProfessional)
        assert healthcare_professional.public_id == healthcare_professional_public_id


if __name__ == '__main__':
    unittest.main()

