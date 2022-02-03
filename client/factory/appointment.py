from typing import List, Dict, Any
from client.util.datetime import DateTimeUtil
from client.enum.position_type import PositionType
from client.enum.appointment_status import AppointmentStatus
from client.model.appointment import Appointment
from client.model.patient import Patient
from client.model.healthcare_professional import HealthcareProfessional

class AppointmentFactory:

    @staticmethod
    def from_appointment_api_response(payload: Dict[str, Any]) -> Appointment:
        '''
        Produces an appointment instance from the appointment API response

        :param payload - The payload from the API response
        :return Appointment - An appointment instacne
        '''
        type = payload['type'] or ''
        status = payload['status'] or AppointmentStatus.pending.value
        patient_id = payload['patient_id'] or ''
        healthcare_professional_id = payload['healthcare_professional_id'] or ''
        start_time = payload['start_time'] or ''
        end_time = payload['end_time'] or ''
        public_id = payload['public_id'] or ''
        patient = payload['patient'] or {}
        healthcare_professional = payload['healthcare_professional'] or {}

        appointment = Appointment()
        appointment.type = type
        appointment.status = status
        appointment.patient_id = patient_id
        appointment.healthcare_professional_id = healthcare_professional_id
        appointment.start_time = DateTimeUtil.from_iso_datetime_string(start_time) if start_time != '' else None
        appointment.end_time = DateTimeUtil.from_iso_datetime_string(end_time) if end_time != '' else None
        appointment.public_id = public_id

        if patient:
            _patient = Patient()
            _patient_public_id = patient['public_id'] or ''
            _patient_name = patient['name'] or ''
            _patient_address = patient['address'] or ''
            _patient_phone = patient['phone'] or ''
            _patient.public_id = _patient_public_id
            _patient.name = _patient_name
            _patient.address = _patient_address
            _patient.phone = _patient_phone
            appointment.patient = patient

        if healthcare_professional:
            _healthcare_professional = HealthcareProfessional()
            _healthcare_professional_public_id = healthcare_professional['public_id'] or ''
            _healthcare_professional_name = healthcare_professional['name'] or ''
            _healthcare_professional_employee_number = healthcare_professional['employee_number'] or ''
            _healthcare_professional_position = healthcare_professional['position'] or PositionType.staff.value
            _healthcare_professional.public_id = _healthcare_professional_public_id
            _healthcare_professional.name = _healthcare_professional_name
            _healthcare_professional.employee_number = _healthcare_professional_employee_number
            _healthcare_professional.position = _healthcare_professional_position
            appointment.healthcare_professional = _healthcare_professional

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

