from typing import List, Dict, Any
from ..config import Config
from .base_service import BaseService
from client.util.datetime import DateTimeUtil
from client.model.appointment import Appointment
from client.factory.appointment import AppointmentFactory
from client.exception.api_call_exception import ApiCallException
from client.enum.appointment_status import AppointmentStatus

class AppointmentService(BaseService):

    def __init__(self, config: Config, headers: Dict) -> None:
        super().__init__(config, headers)

    def make_an_appointment(self, appointment: Appointment) -> Dict[str, Any]:
        '''
        Makes an appointment record

        :param appointment - The appointment record to be saved into the system
        :returns result - The data from the API response
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = self.config.APPOINTMENT_API_MAKE_AN_APPOINTMENT_RESOURCE_URL
        try:
            payload = {
                'type': appointment.type,
                'patient_id': appointment.patient_id,
                'healthcare_professional_id': appointment.healthcare_professional_id,
                'start_time': DateTimeUtil.serialize_datetime_object(appointment.start_time),
                'end_time': DateTimeUtil.serialize_datetime_object(appointment.end_time),
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
            print(f'{self.__class__.__name__} - make_an_appointment - captured an exception:')
            print(e)
            raise e

    def cancel_an_appointment(self, appointment: Appointment) -> Dict[str, Any]:
        '''
        Cancels an appointment record

        :param appointment - The appointment record to be cancelled from the system
        :returns result - The data from the API response
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = f'{self.config.APPOINTMENT_API_CANCEL_AN_APPOINTMENT_RESOURCE_URL}/{appointment.public_id}'
        try:
            payload = {
                'status': appointment.status,
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
            print(f'{self.__class__.__name__} - cancel_an_appointment - captured an exception:')
            print(e)
            raise e

    def perform_consulting_service(self, public_id: str) -> Dict[str, Any]:
        '''
        Performs consulting service for the appointment

        :param public_id - The identifier of the appointment record to be changed to the system
        :returns result - The data from the API response
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = f'{self.config.APPOINTMENT_API_UPDATE_STATUS_OF_AN_APPOINTMENT_RESOURCE_URL}/{public_id}'
        try:
            payload = {
                'status': AppointmentStatus.consulting.value,
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
            print(f'{self.__class__.__name__} - perform_consulting_service - captured an exception:')
            print(e)
            raise e

    def change_appointment_status(self, public_id: str, data: Dict = {}) -> Dict[str, Any]:
        '''
        Changes the status of the appointment

        :param public_id - The identifier of the appointment record to be changed to the system
        :returns result - The data from the API response
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = f'{self.config.APPOINTMENT_API_UPDATE_STATUS_OF_AN_APPOINTMENT_RESOURCE_URL}/{public_id}'
        try:
            payload = {
                'status': data['status'] or AppointmentStatus.pending.value,
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
            print(f'{self.__class__.__name__} - perform_consulting_service - captured an exception:')
            print(e)
            raise e

    def get_appointment_list(self, healthcare_professional_id: str = None) -> List[Appointment]:
        '''
        Gets the list of appointment

        :param healthcare_professional_id - The healthcare professional ID
        :return appointment_list - The list of appointment
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = self.config.APPOINTMENT_API_GET_APPOINTMENT_LIST_RESOURCE_URL
        params = {}

        if healthcare_professional_id is not None:
            resource_url += '/'
            params = {
                'healthcare_professional_id': healthcare_professional_id,
            }

        try:
            status_code, data = self.get(resource_url, params=params)
            is_success = data['is_success']
            message = data['message']

            if status_code == 200 and is_success:
                payload = data['payload']
                return AppointmentFactory.from_appointment_list_api_response(payload)
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - get_appointment_list - captured an exception:')
            print(e)
            raise e

    def get_appointment(self, public_id: str) -> Appointment:
        '''
        Gets a appointment

        :param public_id - The public accessible ID of the appointment record
        :return appointment - The appointment
        :throws UnauthenticatedException | ApiCallException | Exception
        '''
        resource_url = f'{self.config.APPOINTMENT_API_GET_APPOINTMENT_DETAILS_RESOURCE_URL}/{public_id}'
        try:
            status_code, data = self.get(resource_url)
            is_success = data['is_success']
            message = data['message']

            if status_code == 200 and is_success:
                payload = data['payload']
                return AppointmentFactory.from_appointment_api_response(payload)
            else:
                raise ApiCallException(message)

        except Exception as e:
            print(f'{self.__class__.__name__} - get_appointment - captured an exception:')
            print(e)
            raise e

