from typing import Dict
from client.enum.position_type import PositionType
from client.model.employee import Employee
from client.model.nurse import Nurse
from client.model.doctor import Doctor
from client.model.receptionist import Receptionist


class EmployeeFactory:

    @staticmethod
    def from_user_info_response(payload: Dict[str, str]) -> Employee:
        '''
        Produce an employee instance from the user info API response
        '''
        name = payload['name'] or ''
        employee_number = payload['employee_number'] or ''
        position = payload['position'] or PositionType.staff.value

        employee = None
        if position == PositionType.receptionist.value:
            employee = Receptionist()
        elif position == PositionType.doctor.value:
            employee = Doctor()
        elif position == PositionType.nurse.value:
            employee = Nurse()
        else:
            employee = Employee()

        employee.name = name
        employee.employee_number = employee_number
        return employee

