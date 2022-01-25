from .. import db
from sqlalchemy.sql import func
from app.main.enum.appointment_type import AppointmentType


class Appointment(db.Model):
    ''' Appointment Model for storing appointment related details '''
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(1), nullable=True, default=AppointmentType.standard.value)
    healthcare_professional_id = db.Column(db.String, db.ForeignKey('user.public_id'))
    patient_id = db.Column(db.String, db.ForeignKey('patient.public_id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    booked_on = db.Column(db.DateTime, nullable=False, default=func.now())
    public_id = db.Column(db.String(100), unique=True)

    def __str__(self):
        return f"<Appointment starts at '{self.start_time}' and ends at '{self.end_time}'>"

    def __repr__(self):
        return f"""
            Appointment: (
                id: {self.id},
                type: {self.type},
                healthcared_professional_id: {self.healthcare_professional_id},
                patient_id: {self.patient_id},
                start_time: {self.start_time},
                end_time: {self.end_time},
                booked_on: {self.booked_on},
                public_id: {self.public_id},
            )
        """
