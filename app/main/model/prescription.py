from .. import db
from sqlalchemy.sql import func
from app.main.enum.prescription_type import PrescriptionType


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
