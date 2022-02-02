from typing import List, Dict, Any
from client.enum.position_type import PositionType
from client.model.employee import Employee
from client.model.nurse import Nurse
from client.model.doctor import Doctor
from client.model.receptionist import Receptionist


class EmployeeFactory:

    @staticmethod
    def from_user_api_response(payload: Dict[str, Any]) -> Employee:
        '''
        Produces an employee instance from the user API response

        :param payload - The payload from the API response
        :return employee - An employee instance
        '''
        public_id = payload['public_id'] or ''
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

        employee.public_id = public_id
        employee.name = name
        employee.employee_number = employee_number
        employee.position = position

        return employee

    @staticmethod
    def from_user_list_api_response(payload: List[Dict[str, Any]]) -> List[Employee]:
        '''
        Produces a list of employee instance from the user list API response

        :param payload - The payload from the API response
        :return employee_list - The list of employee instance
        '''
        employee_list = []

        for data in payload:
            employee = EmployeeFactory.from_user_api_response(data)
            employee_list.append(employee)

        return employee_list

