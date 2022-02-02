from client.enum.position_type import PositionType


class Employee:

    def __init__(self) -> None:
        self._public_id = ''
        self._name = ''
        self._position = PositionType.staff.value
        self._employee_number = ''

        self._is_authenticated = False
        self._is_active = False
        self._is_anonymous = False
        self._access_token = None

    @property
    def public_id(self) -> str:
        return self._public_id

    @public_id.setter
    def public_id(self, new_public_id: str) -> None:
        self._public_id = new_public_id

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

    @property
    def is_authenticated(self) -> bool:
        return self._is_authenticated

    @is_authenticated.setter
    def is_authenticated(self, new_is_authenticated: bool) -> None:
        self._is_authenticated = new_is_authenticated

    @property
    def is_active(self) -> bool:
        return self._is_active

    @is_active.setter
    def is_active(self, new_is_active: bool) -> None:
        self._is_active = new_is_active

    @property
    def is_anonymous(self) -> bool:
        return self._is_anonymous

    @is_anonymous.setter
    def is_anonymous(self, new_is_anonymous: bool) -> None:
        self._is_anonymous = new_is_anonymous

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, new_access_token: str) -> None:
        self._access_token = new_access_token

    def get_id(self) -> str:
        return self.access_token

    def __str__(self):
        return f'<{self.__class__.__name__} name: {self.name}>'

    def __repr__(self):
        return f'''
            {self.__class__.__name__}: (
                public_id: {self.public_id},
                name: {self.name},
                employee_number: {self.employee_number},

                is_authenticated: {self.is_authenticated},
                is_active: {self.is_active},
                is_anonymous: {self.is_anonymous},
                access_token: {self.access_token},
            )
        '''

