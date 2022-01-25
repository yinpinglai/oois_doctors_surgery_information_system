from .. import db
from sqlalchemy.sql import func


class Patient(db.Model):
	""" Patient Model for storing patient related details"""
	__tablename__ = "patient"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), unique=True, nullable=False)
	address = db.Column(db.String(255), nullable=False)
	phone = db.Column(db.String(255), nullable=False)
	registered_on = db.Column(db.DateTime, nullable=False, default=func.now())
	public_id = db.Column(db.String(100), unique=True)

	def __str__(self):
		return f"<Patient '{self.name}'>"

	def __repr__(self):
		return f"""
			Patient: (
				id: {self.id},
				name: {self.name},
				address: {self.address},
				phone: {self.phone},
			)
		"""
