from typing import List, Dict

from ..config import Config
from .base_service import BaseService
from client.enum.position_type import PositionType
from client.factory.employee import EmployeeFactory
from client.exception.api_call_exception import ApiCallException
from client.model.healthcare_professional import HealthcareProfessional


class HealthcareProfessionalService(BaseService):

    def __init__(self, config: Config, headers: Dict) -> None:
        super().__init__(config, headers)


    def get_healthcare_professional_list(self) -> List[HealthcareProfessional]:
        '''
        Gets the list of healthcare professionals

        :return health_professional_list - The list of healthcare professional
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = self.config.HEALTHCARE_PROFESSIONAL_API_GET_HEALTHCARE_PROFESSIONAL_LIST_RESOURCE_URL
        try:
            params = {
                'position': [
                    PositionType.doctor.value,
                    PositionType.nurse.value,
                ],
            }
            headers = {}
            status_code, data = self.get(resource_url, headers, params)
            is_success = data['is_success']
            message = data['message']

            if status_code == 200 and is_success:
                payload = data['payload']
                return EmployeeFactory.from_user_list_api_response(payload)
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - get_health_professional_list - captured an exception:')
            print(e)
            raise e


    def get_healthcare_professional(self, public_id: str) -> HealthcareProfessional:
        '''
        Gets a healthcare professional's details

        :return health_professional - A healthcare professional instance
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = f'{self.config.HEALTHCARE_PROFESSIONAL_API_GET_HEALTHCARE_PROFESSIONAL_RESOURCE_URL}/{public_id}'
        try:
            status_code, data = self.get(resource_url)
            is_success = data['is_success']
            message = data['message']

            if status_code == 200 and is_success:
                payload = data['payload']
                return EmployeeFactory.from_user_api_response(payload)
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - get_health_professional_list - captured an exception:')
            print(e)
            raise e



