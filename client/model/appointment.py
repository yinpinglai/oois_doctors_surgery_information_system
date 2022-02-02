from datetime import datetime


class Appointment:

    def __init__(self) -> None:
        self._type = ''
        self._patient_id = ''
        self._healthcare_professional_id = ''
        self._start_time = None
        self._end_time = None
        self._public_id = ''

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, new_type: str) -> None:
        self._type = new_type

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

    def __str__(self):
        return f'<Appointment for patient {self.patient_id} will be consulted by the healthcared professional {self.healthcare_professional_id}>'

    def __repr__(self):
        return f'''
            Appointment: (
                type: {self.type},
                patient_id: {self.patient_id},
                healthcare_professional_id: {self.healthcare_professional_id},
                start_time: {self.start_time},
                end_time: {self.end_time},
                public_id: {self.public_id},
            )
        '''
