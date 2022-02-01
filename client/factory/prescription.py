from typing import Dict, Any, List
from client.util.datetime import DateTimeUtil
from client.model.prescription import Prescription


class PrescriptionFactory:

    @staticmethod
    def from_prescription_api_response(payload: Dict[str, Any]) -> Prescription:
        '''
        Produces a prescription instance from the prescription API response

        :param payload - The payload from the API response
        :return prescription - A prescription instance
        '''
        type = payload['type'] or ''
        patient_id = payload['patient_id'] or ''
        doctor_id = payload['doctor_id'] or ''
        quantity = payload['quantity'] or 0
        dosage = payload['dosage'] or ''
        created_on = payload['created_on'] or ''
        public_id = payload['public_id'] or ''

        prescription = Prescription()
        prescription.type = type
        prescription.patient_id = patient_id
        prescription.doctor_id = doctor_id
        prescription.quantity = quantity
        prescription.dosage = dosage
        prescription.public_id = public_id
        prescription.created_on = DateTimeUtil.from_iso_datetime_string(created_on) if created_on != '' else None
        return prescription

    @staticmethod
    def from_prescription_list_api_response(payload: List[Dict[str, Any]]) -> List[Prescription]:
        '''
        Produces the list of prescription instance from the list of the prescription API response

        :param payload - The payload from the API response
        :return prescription_list - The list of the prescription instance
        '''
        prescription_list = []

        for data in payload:
            prescription = PrescriptionFactory.from_prescription_api_response(data)
            prescription_list.append(prescription)

        return prescription_list
