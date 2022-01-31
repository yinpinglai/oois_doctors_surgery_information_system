import uuid
import datetime

from app.main import db
from app.main.model.user import User
from app.main.model.patient import Patient
from app.main.model.prescription import Prescription
from app.main.enum.prescription_type import PrescriptionType
from app.main.util.response import ResponseUtil
from typing import Dict, Tuple


def save_new_prescription(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    doctor = User.query.filter_by(public_id=data['doctor_id']).first()
    patient = Patient.query.filter_by(public_id=data['patient_id']).first()

    if not doctor:
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=False,
            message='Doctor record not found. Please check.',
        )
        return response_object, 409
    elif not patient:
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=False,
            message='Patient record not found. Please create a patient record first.',
        )
        return response_object, 409
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
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=True,
            message='Successfully issued.',
            payload={
                'id': new_prescription.public_id,
            },
        )
        return response_object, 201


def update_a_prescription(public_id: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    prescription = Prescription.query.filter_by(public_id=public_id).first()

    if not prescription:
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=False,
            message='Prescription record not found. Please create a new record first.',
        )
        return response_object, 404
    else:
        type = data['type'] if 'type' in data else prescription.type

        if type != PrescriptionType.standard.value and type != PrescriptionType.repeatable.value:
            response_object = ResponseUtil.produce_common_response_dict(
                is_success=False,
                message=f'Unsupported prescription type: {type} found.'
            )
            return response_object, 409

        quantity = data['quantity'] if 'quantity' in data else prescription.quantity
        dosage = data['dosage'] if 'dosage' in data else prescription.dosage

        prescription.type = type
        prescription.quantity = quantity
        prescription.dosage = dosage

        save_changes(prescription)
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=True,
            message='Successfully updated.',
            payload={
                'id': prescription.public_id,
            }
        )
        return response_object, 201

def get_all_prescritpions() -> Tuple[Dict[str, str], int]:
    prescriptions = Prescription.query.all()
    prescriptions = [prescription.serialize() for prescription in prescriptions]
    response_object = ResponseUtil.produce_common_response_dict(
        is_success=True,
        message='Successfully fetched.',
        payload=prescriptions,
    )
    return response_object, 200


def get_a_prescription(public_id: str) -> Tuple[Dict[str, str], int]:
    prescription = Prescription.query.filter_by(public_id=public_id).first()
    response_object = ResponseUtil.produce_common_response_dict(
        is_success=True,
        message='Successfully fetched.',
        payload=prescription,
    )
    return response_object, 200


def save_changes(data: Prescription) -> None:
    db.session.add(data)
    db.session.commit()
