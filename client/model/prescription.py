from datetime import datetime

class Prescription:

    def __init__(self) -> None:
        self._type = ''
        self._patient_id = ''
        self._doctor_id = ''
        self._quantity = 0
        self._dosage = ''
        self._created_on = None
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
    def doctor_id(self) -> str:
        return self._doctor_id

    @doctor_id.setter
    def doctor_id(self, new_doctor_id: str) -> None:
        self._doctor_id = new_doctor_id

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, new_quantity: int) -> None:
        self._quantity = new_quantity

    @property
    def dosage(self) -> str:
        return self._dosage

    @dosage.setter
    def dosage(self, new_dosage: str) -> None:
        self._dosage = new_dosage

    @property
    def created_on(self) -> str:
        return self._created_on

    @created_on.setter
    def created_on(self, new_created_on: datetime) -> None:
        self._created_on = new_created_on

    @property
    def public_id(self) -> str:
        return self._public_id

    @public_id.setter
    def public_id(self, new_public_id: str) -> None:
        self._public_id = new_public_id

    def __str__(self):
        return f'<Prescription for patient {self.patient_id} issued by the doctor {self.doctor_id}>'

    def __repr__(self):
        return f'''
            Prescription: (
                type: {self.type},
                patient_id: {self.patient_id},
                doctor_id: {self.doctor_id},
                quantity: {self.quantity},
                dosage: {self.dosage},
                created_on: {self.created_on},
                public_id: {self.public_id},
            )
        '''
