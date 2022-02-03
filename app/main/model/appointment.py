from sqlalchemy.sql import func
from .. import db
from .json_serializable import JSONSerializable
from app.main.util.datetime import DateTimeUtil
from app.main.enum.appointment_type import AppointmentType
from app.main.enum.appointment_status import AppointmentStatus


@JSONSerializable.register
class Appointment(db.Model):
    ''' Appointment Model for storing appointment related details '''
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(1), nullable=True, default=AppointmentType.standard.value)
    status = db.Column(db.Integer, nullable=True, default=AppointmentStatus.pending.value)
    healthcare_professional_id = db.Column(db.String, db.ForeignKey('user.public_id'))
    patient_id = db.Column(db.String, db.ForeignKey('patient.public_id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    booked_on = db.Column(db.DateTime, nullable=False, default=func.now())
    public_id = db.Column(db.String(100), unique=True)
    patient = db.relationship('Patient', viewonly=True)
    healthcare_professional = db.relationship('User', viewonly=True)

    def serialize(self):
        '''
        Serializes the object instance to the JSON standard format

        :return serialized_dictionary - The serialized JSON dictionary
        '''
        return {
            'id': self.id,
            'type': self.type,
            'healthcare_professional_id': self.healthcare_professional_id,
            'patient_id': self.patient_id,
            'start_time': DateTimeUtil.serialize_datetime_object(self.start_time),
            'end_time': DateTimeUtil.serialize_datetime_object(self.end_time),
            'booked_on': DateTimeUtil.serialize_datetime_object(self.booked_on),
            'public_id': self.public_id,
        }

    def __str__(self):
        return f"<Appointment starts at '{self.start_time}' and ends at '{self.end_time}'>"

    def __repr__(self):
        return f"""
            Appointment: (
                id: {self.id},
                type: {self.type},
                status: {self.status},
                healthcared_professional_id: {self.healthcare_professional_id},
                patient_id: {self.patient_id},
                start_time: {self.start_time},
                end_time: {self.end_time},
                booked_on: {self.booked_on},
                public_id: {self.public_id},
            )
        """
