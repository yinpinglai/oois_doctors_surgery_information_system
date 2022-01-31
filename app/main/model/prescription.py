from .. import db
from typing import Dict, Any
from sqlalchemy.sql import func
from app.main.util.datetime import DateTimeUtil
from app.main.enum.prescription_type import PrescriptionType
from .json_serializable import JSONSerializable


@JSONSerializable.register
class Prescription(db.Model):
    ''' Prescription Model for storing prescription related details '''
    __tablename__ = 'prescription'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(1), nullable=False, default=PrescriptionType.standard.value)
    patient_id = db.Column(db.String, db.ForeignKey('patient.public_id'))
    doctor_id = db.Column(db.String, db.ForeignKey('user.public_id'))
    quantity = db.Column(db.Integer, nullable=False, default=0)
    dosage = db.Column(db.String(255), nullable=False, default=0.0)
    created_on = db.Column(db.DateTime, nullable=False, default=func.now())
    public_id = db.Column(db.String(100), unique=True)

    def serialize(self) -> Dict[str, Any]:
        '''
        Serializes the object instance to the JSON standard format

        :return serialized_dictionary - The serialized JSON dictionary
        '''
        return {
            'id': self.id,
            'type': self.type,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'quantity': self.quantity,
            'dosage': self.dosage,
            'created_on': DateTimeUtil.serialize_datetime_object(self.created_on),
            'public_id': self.public_id,
        }

    def __str__(self):
        return f"<Prescription '{self.public_id}'>"

    def __repr__(self):
        return f"""
            Prescription: (
                id: {self.id},
                patient_id: {self.patient_id},
                doctor_id: {self.doctor_id},
                quantity: {self.quantity},
                dosage: {self.dosage},
                created_on: {self.created_on},
            )
        """
