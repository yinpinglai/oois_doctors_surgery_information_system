import unittest

from client.config import config_by_name
from client.service.auth_service import AuthService

class TestAuthService(unittest.TestCase):

    def test_login(self):
        config = config_by_name['test']
        auth_service = AuthService(config)

        is_success, token = auth_service.login(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )
        assert is_success == True
        assert token is not None
        assert len(token) > 0
        self.access_token = token


    def test_logout(self):
        config = config_by_name['test']
        auth_service = AuthService(config)

        is_success, token = auth_service.login(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )
        assert is_success == True
        assert token is not None
        assert len(token) > 0

        is_success = auth_service.logout(token)
        assert is_success == True


    def test_user_info(self):
        config = config_by_name['test']
        auth_service = AuthService(config)

        is_success, token = auth_service.login(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )
        assert is_success == True
        assert token is not None
        assert len(token) > 0

        employee = auth_service.user_info(token)
        assert employee is not None
        assert employee.name == 'Kris, Lai'
        assert employee.employee_number == 'sf001'


if __name__ == '__main__':
    unittest.main()

