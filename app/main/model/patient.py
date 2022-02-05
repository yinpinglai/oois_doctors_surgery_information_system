from .. import db
from typing import Dict, Any
from sqlalchemy.sql import func
from app.main.util.datetime import DateTimeUtil
from .json_serializable import JSONSerializable


@JSONSerializable.register
class Patient(db.Model):
    ''' Patient Model for storing patient related details '''
    __tablename__ = 'patient'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=func.now())
    public_id = db.Column(db.String(100), nullable=False, unique=True)
    prescriptions = db.relationship('Prescription')
    appointments = db.relationship('Appointment')

    def serialize(self) -> Dict[str, Any]:
        '''
        Serializes the object instance to the JSON standard format

        :return serialized_dictionary - The serialized JSON dictionary
        '''
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'registered_on': DateTimeUtil.serialize_datetime_object(self.registered_on),
            'public_id': self.public_id,
            'prescriptions': self.prescriptions,
            'appointments': self.appointments,
        }

    def __str__(self):
        return f"<Patient '{self.name}'>"

    def __repr__(self):
        return f"""
            Patient: (
                id: {self.id},
                name: {self.name},
                address: {self.address},
                phone: {self.phone},
                prescriptions: {repr(self.prescriptions)},
                appointments: {repr(self.appointments)},
            )
        """
