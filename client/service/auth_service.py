from typing import Dict, Tuple
from ..config import Config
from .base_service import BaseService
from client.model.employee import Employee
from client.enum.position_type import PositionType
from client.factory.employee import EmployeeFactory
from client.exception.unauthenticated_exception import UnauthenticatedException

class AuthService(BaseService):

    def __init__(self, config: Config, headers: Dict = {}) -> None:
        super().__init__(config, headers)


    def login(self, email: str, password: str) -> Tuple[bool, str or None]:
        '''
        Authenticate the user to the system

        :param email - the email for login
        :param password - the password for login
        :return [is_success, payload] - the result of the authentication
        '''
        resource_url = self.config.AUTH_API_LOGIN_RESOURCE_URL
        payload = {
            'email': email,
            'password': password,
        }
        try:
            status_code, data = self.post(resource_url, payload)
            if status_code == 200:
                token = data['payload']['Authorization']
                return True, token
            return False, None
        except:
            return False, None


    def logout(self, token: str) -> bool:
        '''
        Logout user from the system

        :param token - the access token
        :return is_success - the result of calling the logout API
        '''
        resource_url = self.config.AUTH_API_LOGOUT_RESOURCE_URL
        try:
            self.set_headers({
                'Authorization': token,
            })
            status_code, _ = self.post(resource_url)
            return status_code == 200
        except:
            return False


    def user_info(self, token: str) -> Employee:
        '''
        Get logged in user info from the system

        :param token - the access token
        :return employee - an employee instance
        '''
        resource_url = self.config.AUTH_API_USER_INFO_URL
        try:
            self.set_headers({
                'Authorization': token,
            })
            status_code, data = self.post(resource_url)
            is_success = data['is_success']

            if status_code == 200 and is_success:
                payload = data['payload']
                return EmployeeFactory.from_user_info_response(payload)

            raise UnauthenticatedException()
        except:
            raise UnauthenticatedException()
