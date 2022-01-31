import uuid
import datetime
from dateutil import parser

from app.main import db
from app.main.model.user import User
from app.main.model.patient import Patient
from app.main.model.appointment import Appointment
from app.main.enum.appointment_type import AppointmentType
from app.main.util.response import ResponseUtil
from typing import Dict, Tuple


def save_new_appointment(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    healthcare_professional = User.query.filter_by(public_id=data['healthcare_professional_id']).first()
    patient = Patient.query.filter_by(public_id=data['patient_id']).first()

    if not healthcare_professional:
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=False,
            message='Healthcare professional record not found. Please check.'
        )
        return response_object, 409
    elif not patient:
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=False,
            message='Patient record not found. Please create a patient record first.'
        )
        return response_object, 409
    else:
        start_time = parser.parse(data['start_time'])
        end_time = parser.parse(data['end_time'])
        appointment = Appointment.query.filter_by(
            start_time=start_time,
            end_time=end_time,
        ).first()
        if not appointment:
            new_appointment = Appointment(
                type=data['type'],
                healthcare_professional_id=healthcare_professional.public_id,
                patient_id=patient.public_id,
                start_time=start_time,
                end_time=end_time,
                booked_on=datetime.datetime.utcnow(),
                public_id=str(uuid.uuid4()),
            )
            save_changes(new_appointment)
            response_object = ResponseUtil.produce_common_response_dict(
                is_success=True,
                message='Successfully booked.',
                payload={
                    'id': new_appointment.public_id,
                }
            )
            return response_object, 201
        else:
            response_object = ResponseUtil.produce_common_response_dict(
                is_success=False,
                message='Requested timeslot is not available.',
            )
            return response_object, 409


def update_an_appointment(public_id: str, data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    appointment = Appointment.query.filter_by(public_id=public_id).first()

    if not appointment:
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=False,
            message='Appointment record not found. Please create a new record first.',
        )
        return response_object, 409
    else:
        type = data['type'] if 'type' in data else appointment.type

        if type != AppointmentType.standard.value and type != AppointmentType.emergency.value:
            response_object = ResponseUtil.produce_common_response_dict(
                is_success=False,
                message=f'Unsupported appointment type: {type} found.',
            )
            return response_object, 409

        healthcare_professional_id = data['healthcare_professional_id'] if 'healthcare_professional_id' in data else appointment.healthcare_professional_id
        healthcare_professional = User.query.filter_by(public_id=healthcare_professional_id).first()

        if not healthcare_professional:
            response_object = ResponseUtil.produce_common_response_dict(
                is_success=False,
                message='Healthcare professional record not found. Please check.',
            )
            return response_object, 409

        start_time = data['start_time'] if 'start_time' in data else appointment.start_time
        end_time = data['end_time'] if 'end_time' in data else appointment.end_time

        parsed_start_time = parser.parse(start_time)
        parsed_end_time = parser.parse(end_time)

        has_booked_appointment = Appointment.query.filter_by(
            start_time=parsed_start_time,
            end_time=parsed_end_time,
        ).first()

        if has_booked_appointment is not None and has_booked_appointment.public_id != appointment.public_id:
            response_object = ResponseUtil.produce_common_response_dict(
                is_success=False,
                message='Requested timeslot is not available.',
            )
            return response_object, 409

        appointment.type = type
        appointment.healthcare_professional_id = healthcare_professional.public_id
        appointment.start_time = parsed_start_time
        appointment.end_time = parsed_end_time

        save_changes(appointment)
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=True,
            message='Successfully updated.',
            payload={
                'id': appointment.public_id,
            },
        )
        return response_object, 201

def delete_an_appointment(public_id: str) -> Tuple[Dict[str, str], int]:
    appointment = Appointment.query.filter_by(public_id=public_id).first()

    response_object = ResponseUtil.produce_common_response_dict(
        is_success=True,
        message='Successfully deleted.'
    )
    if not appointment:
        return response_object, 200
    else:
        db.session.delete(appointment)
        db.session.commit()
        return response_object, 200


def get_all_appointments():
    return Appointment.query.all()


def get_an_appointment(public_id: str):
    return Appointment.query.filter_by(public_id=public_id).first()


def save_changes(data: Appointment) -> None:
    db.session.add(data)
    db.session.commit()
