import uuid
import datetime

from app.main import db
from app.main.model.patient import Patient
from app.main.util.response import produce_common_response_dict
from typing import Dict, Tuple


def save_new_patient(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    patient = Patient.query.filter_by(name=data['name']).first()
    if not patient:
        new_patient = Patient(
            name=data['name'],
            address=data['address'],
            phone=data['phone'],
            public_id=str(uuid.uuid4()),
            registered_on=datetime.datetime.utcnow(),
        )
        save_changes(new_patient)
        response_object = produce_common_response_dict(
            is_success=True,
            message='Successfully registered.',
            payload={
                'id': new_patient.public_id,
            }
        )
        return response_object, 201
    else:
        response_object = produce_common_response_dict(
            is_success=False,
            message='Patient already exists.',
        )
        return response_object, 409


def get_all_patients():
    return Patient.query.all()


def get_a_patient(public_id: str):
    return Patient.query.filter_by(public_id=public_id).first()


def save_changes(data: Patient) -> None:
    db.session.add(data)
    db.session.commit()
