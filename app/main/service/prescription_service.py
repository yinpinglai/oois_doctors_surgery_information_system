import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.model.patient import Patient
from app.main.model.prescription import Prescription
from typing import Dict, Tuple


def save_new_prescription(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
	doctor = User.query.filter_by(public_id=data['doctor_id']).first()
	patient = Patient.query.filter_by(public_id=data['patient_id']).first()

	if not doctor:
		response_object = {
            'status': 'fail',
            'message': 'Doctor record not found. Please check.',
        }
	elif not patient:
		response_object = {
            'status': 'fail',
            'message': 'Patient record not found. Please create a patient record',
        }
	else:
		new_prescription = Prescription(
			type=data['type'],
			patient_id=patient.public_id,
			doctor_id=doctor.public_id,
			quantity=data['quantity'],
			dosage=data['dosage'],
			public_id=str(uuid.uuid4()),
			created_on=datetime.datetime.utcnow(),
		)
		save_changes(new_prescription)
		return {
            'status': 'success',
            'message': 'Successfully issued.',
			'id': new_prescription.public_id,
        }, 201
	return response_object, 409


def update_a_prescription(public_id, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
	prescription = Prescription.query.filter_by(public_id=public_id).first()

	if not prescription:
		response_object = {
            'status': 'fail',
            'message': 'Prescription record not found. Please create a new record.',
        }
	else:
		type = data['type'] if 'type' in data else prescription.type
		quantity = data['quantity'] if 'quantity' in data else prescription.quantity
		dosage = data['dosage'] if 'dosage' in data else prescription.dosage

		prescription.type = type
		prescription.quantity = quantity
		prescription.dosage = dosage

		save_changes(prescription)
		return {
            'status': 'success',
            'message': 'Successfully updated.',
			'id': prescription.public_id,
        }, 201
	return response_object, 409

def get_all_prescritpions():
	return Prescription.query.all()


def get_a_prescription(public_id):
	return Prescription.query.filter_by(public_id=public_id).first()


def save_changes(data: Prescription) -> None:
    db.session.add(data)
    db.session.commit()
