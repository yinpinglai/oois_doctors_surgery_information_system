from typing import Any, Dict
from ..config import Config
from .base_service import BaseService
from client.model.prescription import Prescription
from client.exception.api_call_exception import ApiCallException


class PrescriptionService(BaseService):

    def __init__(self, config: Config, headers: Dict) -> None:
        super().__init__(config, headers)

    def issue_prescription(self, prescription: Prescription) -> Dict[str, Any]:
        '''
        Issues a new prescription record for patient by the doctor

        :param prescription - The prescription record to be saved into system
        :returns result - The data from the API response
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = self.config.PRESCRIPTION_API_ISSUE_PRESCRIPTION_RESOURCE_URL
        try:
            payload = {
                'type': prescription.type,
                'patient_id': prescription.patient_id,
                'doctor_id': prescription.doctor_id,
                'quantity': prescription.quantity,
                'dosage': prescription.dosage,
            }
            status_code, data = self.post(resource_url, payload=payload)
            is_success = data['is_success']
            message = data['message']

            if status_code == 201 and is_success:
                payload = data['payload']
                return payload
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - issue_prescription - captured an exception:')
            print(e)
            raise e


    def request_an_repeatable_prescription(self, prescription: Prescription) -> Dict[str, Any]:
        '''
        Makes a request of changing the type of prescription to be a repeatable prescription

        :param prescription - The prescription record to be changed its type to a repeatable
        :returns result - The data from API response
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = f'{self.config.PRESCRIPTION_API_REQUEST_AN_REPEATABLE_PRESCRIPTION_RESOURCE_URL}/{prescription.public_id}'
        try:
            payload = {
                'type': prescription.type,
            }
            status_code, data = self.put(resource_url, payload=payload)
            is_success = data['is_success']
            message = data['message']

            if status_code == 201 and is_success:
                payload = data['payload']
                return payload
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - request_an_repeatable_prescription - captured an exception:')
            print(e)
            raise e
