import uuid
import datetime
from dateutil import parser

from typing import Dict, Tuple
from app.main import db
from app.main.model.user import User
from app.main.model.patient import Patient
from app.main.model.appointment import Appointment
from app.main.enum.appointment_type import AppointmentType
from app.main.util.response import ResponseUtil
from app.main.util.datetime import DateTimeUtil


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
        status = data['status'] if 'status' in data else appointment.status

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

        parsed_start_time = parser.parse(start_time) if isinstance(start_time, str) else start_time
        parsed_end_time = parser.parse(end_time) if isinstance(end_time, str) else end_time

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
        appointment.status = status
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
        message='Successfully deleted.',
        payload={
            'id': public_id,
        },
    )
    if not appointment:
        return response_object, 200
    else:
        db.session.delete(appointment)
        db.session.commit()
        return response_object, 200


def get_all_appointments(params: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    appointments_query = Appointment.query

    if params and params['healthcare_professional_id'] is not None:
        appointments_query = appointments_query.filter(
            Appointment.healthcare_professional_id == params['healthcare_professional_id']
        )

    if params and params['start_time'] is not None:
        appointments_query = appointments_query.filter(
            Appointment.start_time >= DateTimeUtil.from_iso_datetime_string(params['start_time'])
        )

    if params and params['end_time'] is not None:
        appointments_query = appointments_query.filter(
            Appointment.end_time <= DateTimeUtil.from_iso_datetime_string(params['end_time'])
        )

    if params and params['sort_by'] is not None and params['sort_by'] == 'start_time':
        sort_order = params['sort_order'] or 'asc'
        if sort_order == 'desc':
            appointments_query = appointments_query.order_by(
                Appointment.start_time.desc()
            )
        else:
            appointments_query = appointments_query.order_by(
                Appointment.start_time.asc()
            )

    appointments = ResponseUtil.convert_to_json_serializable(
        appointments_query.all()
    )
    response_object = ResponseUtil.produce_common_response_dict(
        is_success=True,
        message='Successfully fetched.',
        payload=appointments,
    )
    return response_object, 200


def get_an_appointment(public_id: str):
    appointment = ResponseUtil.convert_to_json_serializable(
        Appointment.query.filter_by(public_id=public_id).first()
    )
    response_object = ResponseUtil.produce_common_response_dict(
        is_success=True,
        message='Successfully fetched.',
        payload=appointment,
    )
    return response_object, 200

def get_next_available(params: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    print(params)
    appointments_query = Appointment.query

    if params and params['healthcare_professional_id'] is not None:
        appointments_query = appointments_query.filter(
            Appointment.healthcare_professional_id == params['healthcare_professional_id']
        )

    if params and params['start_time'] is not None:
        appointments_query = appointments_query.filter(
            Appointment.start_time >= DateTimeUtil.from_iso_datetime_string(params['start_time'])
        )

    if params and params['end_time'] is not None:
        appointments_query = appointments_query.filter(
            Appointment.end_time <= DateTimeUtil.from_iso_datetime_string(params['end_time'])
        )

    appointments = appointments_query.all()
    now = datetime.datetime.now()
    date_format = '%Y-%m-%d %H:%M'

    if len(appointments) == 0:
        next_hour = now - datetime.timedelta(
            minutes=now.minute,
            seconds=now.second,
        ) + datetime.timedelta(hours=1)
        next_start_time = next_hour.strftime(date_format)
        next_end_time = (next_hour + datetime.timedelta(hours=1)).strftime(date_format)
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=True,
            message='Successfully fetched.',
            payload={
                'healthcare_professional_id': params['healthcare_professional_id'],
                'start_time': next_start_time,
                'end_time': next_end_time,
            }
        )
        return response_object, 200
    else:
        available_time_slots = []

        clinic_opening_hour = now - datetime.timedelta(
            hours=now.hour,
            minutes=now.minute,
            seconds=now.second,
        ) + datetime.timedelta(hours=9)
        clinic_lunch_hour = clinic_opening_hour + datetime.timedelta(hours=4)
        clinic_after_lunch_hour = clinic_lunch_hour + datetime.timedelta(hours=1)
        clinic_closing_hour = clinic_after_lunch_hour + datetime.timedelta(hours=4)

        while clinic_opening_hour < clinic_lunch_hour:
            available_time_slots.append({
                'start_time': clinic_opening_hour + datetime.timedelta(hours=1),
                'end_time': clinic_opening_hour + datetime.timedelta(hours=2),
            })
            clinic_opening_hour += datetime.timedelta(hours=1)

        while clinic_after_lunch_hour < clinic_closing_hour:
            available_time_slots.append({
                'start_time': clinic_after_lunch_hour + datetime.timedelta(hours=1),
                'end_time': clinic_after_lunch_hour + datetime.timedelta(hours=2),
            })
            clinic_after_lunch_hour += datetime.timedelta(hours=1)

        next_available_time_slot_idx = -1

        for i, time_slot in enumerate(available_time_slots):
            start_time = time_slot['start_time']
            end_time = time_slot['end_time']

            if end_time < now or end_time == now:
                continue

            has_booked = False

            for j, appointment in enumerate(appointments):
                appointment_start_time = DateTimeUtil.to_local_timezone(appointment['start_time'])
                appointment_end_time = DateTimeUtil.to_local_timezone(appointment['end_time'])

                if appointment_end_time < now or appointment_end_time == now:
                    continue

                if appointment_start_time == start_time and appointment_end_time == end_time:
                    has_booked = True

            if not has_booked:
                next_available_time_slot_idx = i + 1
                break

        next_available_time_slot = available_time_slots[next_available_time_slot_idx] if next_available_time_slot_idx < len(available_time_slots) else available_time_slots[next_available_time_slot_idx-1]
        next_start_time = next_available_time_slot['start_time'].strftime(date_format)
        next_end_time = next_available_time_slot['end_time'].strftime(date_format)
        response_object = ResponseUtil.produce_common_response_dict(
            is_success=True,
            message='Successfully fetched.',
            payload={
                'healthcare_professional_id': params['healthcare_professional_id'],
                'start_time': next_start_time,
                'end_time': next_end_time,
            }
        )
        return response_object, 200



def save_changes(data: Appointment) -> None:
    db.session.add(data)
    db.session.commit()
