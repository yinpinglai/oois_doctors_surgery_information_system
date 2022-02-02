from typing import List
from client.enum.position_type import PositionType
from .employee import Employee


class HealthcareProfessional(Employee):

    def __init__(self) -> None:
        super().__init__()
        self._appointments = []

    @property
    def appointments(self) -> List:
        return self._appointments

    @appointments.setter
    def appointments(self, new_appointments) -> None:
        self._appointments = new_appointments

    def get_position(self) -> str:
        if self.position == PositionType.doctor.value:
            return 'Doctor'
        elif self.position == PositionType.nurse.value:
            return 'Nurse'
        else:
            return 'Staff'

    def consultation(self) -> str:
        return f'{self.name} is performing consultation.'

