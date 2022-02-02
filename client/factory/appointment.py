from typing import List, Dict, Any
from client.util.datetime import DateTimeUtil
from client.model.appointment import Appointment


class AppointmentFactory:

    @staticmethod
    def from_appointment_api_response(payload: Dict[str, Any]) -> Appointment:
        '''
        Produces an appointment instance from the appointment API response

        :param payload - The payload from the API response
        :return Appointment - An appointment instacne
        '''
        type = payload['type'] or ''
        patient_id = payload['patient_id'] or ''
        healthcare_professional_id = payload['healthcare_professional_id'] or ''
        start_time = payload['start_time'] or ''
        end_time = payload['end_time'] or ''
        public_id = payload['public_id'] or ''

        appointment = Appointment()
        appointment.type = type
        appointment.patient_id = patient_id
        appointment.healthcare_professional_id = healthcare_professional_id
        appointment.start_time = DateTimeUtil.from_iso_datetime_string(start_time) if start_time != '' else None
        appointment.end_time = DateTimeUtil.from_iso_datetime_string(end_time) if end_time != '' else None
        appointment.public_id = public_id
        return appointment


    @staticmethod
    def from_appointment_list_api_response(payload: List[Dict[str, Any]]) -> List[Appointment]:
        '''
        Produces a list of appointment instance from the appointment list API response

        :param payload - The payload from the API response
        :return appointment_list - The list of appointment instance
        '''
        appointment_list = []

        for data in payload:
            appointment = AppointmentFactory.from_appointment_api_response(data)
            appointment_list.append(appointment)

        return appointment_list

