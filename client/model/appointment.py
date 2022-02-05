from typing import Dict, Any
from datetime import datetime
from client.util.datetime import DateTimeUtil
from client.enum.appointment_type import AppointmentType
from client.enum.appointment_status import AppointmentStatus
from .patient import Patient
from .healthcare_professional import HealthcareProfessional

class Appointment:

    def __init__(self) -> None:
        self._type = ''
        self._status = 1
        self._patient_id = ''
        self._healthcare_professional_id = ''
        self._start_time = None
        self._end_time = None
        self._public_id = ''
        self._patient = None
        self._healthcare_professional = None

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, new_type: str) -> None:
        self._type = new_type

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, new_status: int) -> None:
        self._status = new_status

    @property
    def patient_id(self) -> str:
        return self._patient_id

    @patient_id.setter
    def patient_id(self, new_patient_id: str) -> None:
        self._patient_id = new_patient_id

    @property
    def healthcare_professional_id(self) -> str:
        return self._healthcare_professional_id

    @healthcare_professional_id.setter
    def healthcare_professional_id(self, new_healthcare_professional_id: str) -> None:
        self._healthcare_professional_id = new_healthcare_professional_id

    @property
    def start_time(self) -> datetime:
        return self._start_time

    @start_time.setter
    def start_time(self, new_start_time: datetime) -> None:
        self._start_time = new_start_time

    @property
    def end_time(self) -> datetime:
        return self._end_time

    @end_time.setter
    def end_time(self, new_end_time: datetime) -> None:
        self._end_time = new_end_time

    @property
    def public_id(self) -> str:
        return self._public_id

    @public_id.setter
    def public_id(self, new_public_id: str) -> None:
        self._public_id = new_public_id

    @property
    def patient(self) -> Patient:
        return self._patient

    @patient.setter
    def patient(self, new_patient: Patient) -> None:
        self._patient = new_patient

    @property
    def healthcare_professional(self) -> HealthcareProfessional:
        return self._healthcare_professional

    @healthcare_professional.setter
    def healthcare_professional(self, new_healthcare_professional: HealthcareProfessional) -> None:
        self._healthcare_professional = new_healthcare_professional

    def get_type(self) -> str:
        if self.type == AppointmentType.emergency.value:
            return 'Emergency'
        else:
            return 'Standard'

    @property
    def title(self) -> str:
        return f'{self.get_type()} appointment'

    @property
    def url(self) -> str:
        return f'/appointment/{self.public_id}'

    @property
    def event_class(self) -> str:
        if self.type == AppointmentType.emergency.value:
            return 'event-important'
        else:
            return 'event-info'

    @property
    def start(self) -> float:
        if self.start_time is not None:
            localized_start_time = DateTimeUtil.to_local_timezone(self.start_time)
            return localized_start_time.timestamp() * 1000
        return 0

    @property
    def end(self) -> float:
        if self.end_time is not None:
            localized_end_time = DateTimeUtil.to_local_timezone(self.end_time)
            return localized_end_time.timestamp() * 1000
        return 0

    def to_calendar_event(self) -> Dict[str, Any]:
        return {
            'id': self.public_id,
            'title': self.title,
            'url': self.url,
            'class': self.event_class,
            'start': self.start,
            'end': self.end,
            'localized_start_time_string': self.localized_start_time_string,
            'localized_end_time_string': self.localized_end_time_string,
        }

    @property
    def localized_start_time_string(self) -> str:
        if self.start_time:
            localized_start_time = DateTimeUtil.to_local_timezone(self.start_time)
            return localized_start_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ''

    @property
    def localized_end_time_string(self) -> str:
        if self.end_time:
            localized_end_time = DateTimeUtil.to_local_timezone(self.end_time)
            return localized_end_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return ''

    @property
    def is_pending(self) -> bool:
        return self.status == AppointmentStatus.pending.value

    @property
    def is_consulting(self) -> bool:
        return self.status == AppointmentStatus.consulting.value

    @property
    def is_finished(self) -> bool:
        return self.status == AppointmentStatus.finished.value

    @property
    def is_cancelled(self) -> bool:
        return self.status == AppointmentStatus.cancelled.value

    @property
    def is_expired(self) -> bool:
        return self.status == AppointmentStatus.expired.value

    @property
    def current_status(self) -> str:
        if self.is_consulting:
            return 'Consulting'
        elif self.is_finished:
            return 'Completed'
        elif self.is_cancelled:
            return 'Cancelled'
        elif self.is_expired:
            return 'Expired'
        else:
            return 'Pending'

    def __str__(self):
        return f'<Appointment for patient {self.patient_id} will be consulted by the healthcared professional {self.healthcare_professional_id}>'

    def __repr__(self):
        return f'''
            Appointment: (
                type: {self.type},
                status: {self.status},
                patient_id: {self.patient_id},
                healthcare_professional_id: {self.healthcare_professional_id},
                start_time: {self.start_time},
                end_time: {self.end_time},
                public_id: {self.public_id},
                patient: {repr(self.patient)},
                healthcare_professional: {repr(self.healthcare_professional)},
            )
        '''
