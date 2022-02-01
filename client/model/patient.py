from typing import List

class Patient:

    def __init__(self) -> None:
        self._public_id = ''
        self._name = ''
        self._address = ''
        self._phone = ''
        self._appointments = []
        self._prescriptions = []


    @property
    def public_id(self) -> str:
        return self._public_id

    @public_id.setter
    def public_id(self, new_public_id) -> None:
        self._public_id = new_public_id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name) -> None:
        self._name = new_name

    @property
    def address(self) -> str:
        return self._address

    @address.setter
    def address(self, new_address) -> None:
        self._address = new_address

    @property
    def phone(self) -> str:
        return self._phone

    @phone.setter
    def phone(self, new_phone) -> None:
        self._phone = new_phone

    @property
    def appointments(self) -> List:
        return self._appointments

    @property
    def prescriptions(self) -> List:
        return self._prescriptions

    def __str__(self):
        return f'<Patient: {self.name}>'

    def __repr__(self):
        return f'''
            Patient: (
                public_id: {self.public_id},
                name: {self.name},
                address: {self.address},
                phone: {self.phone},
                appointments: {repr(self.appointments)},
                prescriptions: {repr(self.prescriptions)},
            )
        '''

