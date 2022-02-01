from typing import Dict, Any, List
from client.model.patient import Patient
from client.factory.prescription import PrescriptionFactory


class PatientFactory:

    @staticmethod
    def from_patient_api_response(payload: Dict[str, Any]) -> Patient:
        '''
        Produces a patient instance from the patient API response

        :param payload - The payload from the API response
        :return patient - A patient instance
        '''
        public_id = payload['public_id'] or ''
        name = payload['name'] or ''
        address = payload['address'] or ''
        phone = payload['phone'] or ''

        # TODO: enable when the prescription and appointment classes have been implemented
        prescriptions = payload['prescriptions'] or []
        # appointments = payload['appointments'] or []

        patient = Patient()
        patient.public_id = public_id
        patient.name = name
        patient.phone = phone
        patient.address = address
        patient.prescriptions = PrescriptionFactory.from_prescription_list_api_response(prescriptions)
        return patient


    @staticmethod
    def from_patient_list_api_response(payload: List[Dict[str, Any]]) -> List[Patient]:
        '''
        Produces the list of the patient instance from the list of the patient API response

        :param payload - The payload from the API response
        :return patient_list - The list of the patient instance
        '''
        patient_list = []

        for data in payload:
            patient = PatientFactory.from_patient_api_response(data)
            patient_list.append(patient)

        return patient_list

