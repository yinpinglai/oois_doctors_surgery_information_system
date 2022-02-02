from typing import Dict
from flask import Blueprint, render_template, send_from_directory, jsonify
from flask_login import login_required, current_user

from client.util.common import CommonUtil
from client.service.patient_service import PatientService
from client.service.appointment_service import AppointmentService
from client.service.healthcare_professional_service import HealthcareProfessionalService

def create_blueprint(config: Dict[str, str]) -> Blueprint:
    views = Blueprint('views', __name__)

    @views.route('/manifest.json')
    def send_manifest_json():
        return send_from_directory('static/icons', 'manifest.json')

    @views.route('/appointment-schedule', methods=['GET'])
    @login_required
    def appointment_schedule():
        headers = CommonUtil.construct_request_headers(current_user.access_token)
        appointment_service = AppointmentService(config, headers)
        appointments = [appointment.serialize() for appointment in appointment_service.get_appointment_list()]
        resp = jsonify({
            'success' : 1,
            'result' : appointments,
        })
        resp.status_code = 200
        return resp

    @views.route('/', methods=['GET'])
    @login_required
    def home():
        return render_template("home.html", user=current_user)

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

