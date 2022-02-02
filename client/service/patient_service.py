from typing import List, Dict
from ..config import Config
from .base_service import BaseService
from client.model.patient import Patient
from client.factory.patient import PatientFactory
from client.exception.api_call_exception import ApiCallException


class PatientService(BaseService):

    def __init__(self, config: Config, headers: Dict) -> None:
        super().__init__(config, headers)

    def get_patient_list(self) -> List[Patient]:
        '''
        Gets the list of patient

        :return patient_list - The list of patient
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = self.config.PATIENT_API_GET_PATIENT_LIST_RESOURCE_URL
        try:
            status_code, data = self.get(resource_url)
            is_success = data['is_success']
            message = data['message']

            if status_code == 200 and is_success:
                payload = data['payload']
                return PatientFactory.from_patient_list_api_response(payload)
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - get_patient_list - captured an exception:')
            print(e)
            raise e

    def get_patient(self, public_id: str) -> Patient:
        '''
        Gets a patient

        :param public_id - The public accessible ID of the patient record
        :return patient - The patient
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = f'{self.config.PATIENT_API_GET_PATIENT_RESOURCE_URL}/{public_id}'
        try:
            status_code, data = self.get(resource_url)
            is_success = data['is_success']
            message = data['message']

            if status_code == 200 and is_success:
                payload = data['payload']
                return PatientFactory.from_patient_api_response(payload)
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - get_patient - captured an exception:')
            print(e)
            raise e

