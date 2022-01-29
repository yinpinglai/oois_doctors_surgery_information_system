from client.enum.position_type import PositionType


class Employee:

    def __init__(self) -> None:
        self._name = ''
        self._position = PositionType.staff.value
        self._employee_number = ''


    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name

    @property
    def employee_number(self) -> str:
        return self._employee_number

    @employee_number.setter
    def employee_number(self, new_employee_number: str) -> None:
        self._employee_number = new_employee_number

    @property
    def position(self) -> str:
        return self._position

    @position.setter
    def position(self, new_position: str) -> None:
        self._position = new_position

    def __str__(self):
        return f'<{self.__class__.__name__} name: {self.name}>'

    def __repr__(self):
        return f'''
            {self.__class__.__name__}: (
                name: {self.name},
                employee_number: {self.employee_number},
            )
        '''

