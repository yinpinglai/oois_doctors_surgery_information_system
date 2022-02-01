import unittest

from client.config import config_by_name
from client.service.auth_service import AuthService

class TestAuthService(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        config = config_by_name['test']
        self.auth_service = AuthService(config)

    def test_login(self):
        is_success, token = self.auth_service.login(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )
        assert is_success == True
        assert token is not None
        assert len(token) > 0
        self.access_token = token


    def test_logout(self):
        is_success, token = self.auth_service.login(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )
        assert is_success == True
        assert token is not None
        assert len(token) > 0

        is_success = self.auth_service.logout(token)
        assert is_success == True


    def test_user_info(self):
        is_success, token = self.auth_service.login(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )
        assert is_success == True
        assert token is not None
        assert len(token) > 0

        employee = self.auth_service.get_user_info(token)
        assert employee is not None
        assert employee.name == 'Kris, Lai'
        assert employee.employee_number == 'sf001'


if __name__ == '__main__':
    unittest.main()

