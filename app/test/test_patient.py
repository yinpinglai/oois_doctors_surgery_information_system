import json

from app.test.base import BaseTestCase
from app.main.enum.appointment_type import AppointmentType
from app.main.enum.prescription_type import PrescriptionType

def login_as_a_receptionist(self):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )),
        content_type='application/json',
    )

def request_an_repeatable_prescription(self, token: str, prescritpion_id: str):
    return self.client.put(
        f'/api/prescription/{prescritpion_id}',
        headers=dict(
            Authorization=token,
        ),
        data=json.dumps(dict(
            type=PrescriptionType.repeatable.value,
        )),
        content_type='application/json',
    )

def request_an_appointment(self, token: str):
    return self.client.post(
        '/api/appointment/',
        headers=dict(
            Authorization=token,
        ),
        data=json.dumps(dict(
            type=AppointmentType.standard.value,
            patient_id='32cb0bb5-9fa7-49b0-9df2-e30698124af7',
            healthcare_professional_id='67efe526-0bd0-43b9-8d0c-63ff104fcefa',
            start_time='2022-02-03 11:00:00',
            end_time='2022-02-03 12:00:00',
        )),
        content_type='application/json',
    )


class TestPatient(BaseTestCase):

    def test_can_patients_request_an_repeatable_prescription(self):
        ''' Test for patients can request an repeatable prescrtipion '''
        with self.client:
            response = login_as_a_receptionist(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['Authorization'] is not None)

            token = data['payload']['Authorization']

            response = request_an_repeatable_prescription(self, token, prescritpion_id='fabe3b29-40c7-4a08-9254-a5dc707b3d81')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully updated.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['id'] is not None)


    def test_can_patients_request_an_appointment(self):
        ''' Test for patients can request an appointment '''
        with self.client:
            response = login_as_a_receptionist(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['Authorization'] is not None)

            token = data['payload']['Authorization']

            response = request_an_appointment(self, token)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully booked.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['id'] is not None)

