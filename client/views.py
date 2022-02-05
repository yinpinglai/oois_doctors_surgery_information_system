from typing import Dict
from flask import Blueprint, render_template, send_from_directory, request, jsonify, abort, flash, redirect, url_for
from flask_login import login_required, current_user

from client.model.appointment import Appointment
from client.model.prescription import Prescription
from client.enum.appointment_type import AppointmentType
from client.enum.prescription_type import PrescriptionType
from client.util.common import CommonUtil
from client.util.datetime import DateTimeUtil
from client.service.patient_service import PatientService
from client.service.appointment_service import AppointmentService
from client.service.prescription_service import PrescriptionService
from client.service.healthcare_professional_service import HealthcareProfessionalService

def create_blueprint(config: Dict[str, str]) -> Blueprint:
    views = Blueprint('views', __name__)

    @views.route('/manifest.json')
    def send_manifest_json():
        return send_from_directory('static/icons', 'manifest.json')

    @views.route('/', methods=['GET'])
    @login_required
    def home():
        host = f'{config.HOST}:{config.PORT}'
        return render_template('appointment_schedule.html', host=host, user=current_user)

    @views.route('/appointment/new', methods=['GET'])
    @login_required
    def appointment_form():
        args = request.args
        start_time = args['start_time'] if 'start_time' in args else None
        end_time = args['end_time'] if 'end_time' in args else None

        headers = CommonUtil.construct_request_headers(current_user.access_token)
        patient_service = PatientService(config, headers)
        healthcare_professional_service = HealthcareProfessionalService(config, headers)

        patients = patient_service.get_patient_list()
        healthcare_professionals = healthcare_professional_service.get_healthcare_professional_list()

        return render_template(
            'appointment_form.html',
            patients=patients,
            healthcare_professionals=healthcare_professionals,
            start_time=start_time,
            end_time=end_time,
            user=current_user,
        )

    @views.route('/appointment/new/<public_id>', methods=['GET'])
    @login_required
    def appointment_form_for_patient(public_id: str):
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        patient_service = PatientService(config, headers)
        healthcare_professional_service = HealthcareProfessionalService(config, headers)

        patient = patient_service.get_patient(public_id)
        healthcare_professionals = healthcare_professional_service.get_healthcare_professional_list()

        return render_template('appointment_form.html', patient=patient, healthcare_professionals=healthcare_professionals, user=current_user)

    @views.route('/appointment-schedule', methods=['GET'])
    @login_required
    def appointment_schedule():
        args = request.args
        date_from = args['from'] if 'from' in args else None
        date_to = args['to'] if 'to' in args else None

        start_time_iso8601_string = args['start_time'] if 'start_time' in args else None
        end_time_iso8601_string = args['end_time'] if 'end_time' in args else None
        healthcare_professional_id = args['healthcare_professional_id'] if 'healthcare_professional_id' in args else None

        params = {}

        if date_from is not None:
            params['start_time'] = DateTimeUtil.to_iso8601_datetime_string(date_from)
        elif start_time_iso8601_string is not None:
            params['start_time'] = start_time_iso8601_string

        if date_to is not None:
            params['end_time'] = DateTimeUtil.to_iso8601_datetime_string(date_to)
        elif end_time_iso8601_string is not None:
            params['end_time'] = end_time_iso8601_string

        if healthcare_professional_id is not None:
            params['healthcare_professional_id'] = healthcare_professional_id
        else:
            is_healthcare_professional = current_user.is_doctor or current_user.is_nurse
            if is_healthcare_professional:
                params['healthcare_professional_id'] = current_user.public_id

        headers = CommonUtil.construct_request_headers(current_user.access_token)
        appointment_service = AppointmentService(config, headers)
        appointment_list = appointment_service.get_appointment_list(params)
        appointments = [appointment.to_calendar_event() for appointment in appointment_list]
        resp = jsonify({
            'success' : 1,
            'result' : appointments,
        })
        resp.status_code = 200
        return resp

    @views.route('/appointment/next-available', methods=['GET'])
    @login_required
    def appointment_next_available():
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        healthcare_professional_service = HealthcareProfessionalService(config, headers)

        healthcare_professionals = healthcare_professional_service.get_healthcare_professional_list()
        return render_template('find_next_available.html', healthcare_professionals=healthcare_professionals, user=current_user)

    @views.route('/appointment', methods=['POST'])
    @login_required
    def appointments():
        data = request.form
        type = data['type'] or AppointmentType.standard.value
        patient_id = data['patient_id'] or None
        healthcare_professional_id = data['healthcare_professional_id'] or None
        start_time = data['start_time'] or None
        end_time = data['end_time'] or None

        if patient_id is None or healthcare_professional_id is None or start_time is None or end_time is None:
            flash('Required parameter is missing!', category='error')
            return redirect(url_for('views.appointment_form'))

        headers = CommonUtil.construct_request_headers(current_user.access_token)
        appointment_service = AppointmentService(config, headers)

        appointment = Appointment()
        appointment.type = type
        appointment.patient_id = patient_id
        appointment.healthcare_professional_id = healthcare_professional_id
        appointment.start_time = DateTimeUtil.from_iso_datetime_string(start_time)
        appointment.end_time = DateTimeUtil.from_iso_datetime_string(end_time)

        try:
            result = appointment_service.make_an_appointment(appointment)
            if result is not None and result['id'] is not None:
                flash('Made an appointment for patient successfully!', category='success')
        except Exception as e:
            print(e)
            flash('Make an appointment failed, please contact administrators.', category='error')

        return redirect(url_for('views.home'))


    @views.route('/appointment/<public_id>', methods=['GET', 'PUT'])
    @login_required
    def appointment(public_id: str):
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        appointment_service = AppointmentService(config, headers)

        if request.method == 'PUT':
            data = request.json
            if data['status'] is not None:
                try:
                    result = appointment_service.change_appointment_status(public_id, data)
                    resp = jsonify(result)
                    resp.status_code = 201
                    return resp
                except Exception as e:
                    resp = jsonify({ 'is_success': False, 'message': str(e) })
                    resp.status_code = 500
                    return resp

        appointment = appointment_service.get_appointment(public_id)
        return render_template('appointment.html', appointment=appointment, user=current_user)

    @views.route('/prescription', methods=['POST'])
    @login_required
    def prescription():
        if request.method == 'POST':
            data = request.form

            appointment_id = data['appointment_id'] or None
            type = data['type'] if 'type' in data else PrescriptionType.standard.value
            patient_id = data['patient_id'] or None
            doctor_id = current_user.public_id
            quantity = data['quantity'] or 0
            dosage = data['dosage'] or ''

            if patient_id is None or not current_user.is_doctor or appointment_id is None:
                abort(400)

            headers = CommonUtil.construct_request_headers(current_user.access_token)
            prescription_service = PrescriptionService(config, headers)

            prescription = Prescription()
            prescription.type = type
            prescription.patient_id = patient_id
            prescription.doctor_id = doctor_id
            prescription.quantity = int(quantity)
            prescription.dosage = dosage

            try:
                result = prescription_service.issue_prescription(prescription)
                if result is not None and result['id'] is not None:
                    flash('Issued a prescription for patient successfully!', category='success')
            except Exception as e:
                print(e)
                flash('Issue a prescription failed, please contact administrator.', category='error')

            return redirect(url_for('views.appointment', public_id=appointment_id))

        abort(404)

    @views.route('/prescription/<public_id>/type', methods=['PUT'])
    @login_required
    def prescrtipion_details(public_id: str):
        payload = request.json
        patient_id = payload['patient_id'] or None
        type = payload['type'] or None

        if type is None or patient_id is None:
            abort(400)

        headers = CommonUtil.construct_request_headers(current_user.access_token)
        prescription_service = PrescriptionService(config, headers)

        prescription = Prescription()
        prescription.type = type
        prescription.public_id = public_id

        try:
            result = prescription_service.request_an_repeatable_prescription(prescription)
            if result is not None and result['id'] is not None:
                flash('Made an repeatable prescription successfully!', category='success')
        except Exception as e:
            print(e)
            flash('Make an repeatable prescritpion failed, please contact administrator.', category='error')

        return redirect(url_for('views.patient', public_id=patient_id))

    @views.route('/patients', methods=['GET'])
    @login_required
    def patients():
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        patient_service = PatientService(config, headers)

        patients = patient_service.get_patient_list()
        return render_template('patients.html', patients=patients, user=current_user)

    @views.route('/patient/<public_id>', methods=['GET'])
    @login_required
    def patient(public_id: str):
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        patient_service = PatientService(config, headers)

        patient = patient_service.get_patient(public_id)
        return render_template('patient.html', patient=patient, user=current_user)

    @views.route('/healthcare-professionals', methods=['GET'])
    @login_required
    def healthcare_professionals():
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        healthcare_professional_service = HealthcareProfessionalService(config, headers)

        healthcare_professionals = healthcare_professional_service.get_healthcare_professional_list()
        return render_template('healthcare_professionals.html', healthcare_professionals=healthcare_professionals, user=current_user)

    @views.route('/healthcare-professional/<public_id>', methods=['GET'])
    @login_required
    def healthcare_professional(public_id: str):
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        healthcare_professional_service = HealthcareProfessionalService(config, headers)

        healthcare_professional = healthcare_professional_service.get_healthcare_professional(public_id)
        return render_template('healthcare_professional.html', healthcare_professional=healthcare_professional, user=current_user)

    return views

