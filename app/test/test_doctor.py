import json

from app.test.base import BaseTestCase
from app.main.enum.prescription_type import PrescriptionType

def login_as_a_doctor(self):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='kenny.law@gmail.com',
            password='P@ssw0rd',
        )),
        content_type='application/json',
    )

def issue_prescrtipion(self, token):
    return self.client.post(
        '/api/prescription/',
        headers=dict(
            Authorization=token,
        ),
        data=json.dumps(dict(
            type=PrescriptionType.standard.value,
            patient_id='dad6a212-51e2-4b67-9f95-9c9424500863',
            doctor_id='00de28e7-73f9-4099-9edc-7d2f3902d7ba',
            quantity=4,
            dosage='Takes 1 per 4 hours',
        )),
        content_type='application/json',
    )


class TestDoctor(BaseTestCase):

    def test_can_issue_prescrtipion(self):
        ''' Test for doctors can issue a prescrtipion record for patients '''
        with self.client:
            response = login_as_a_doctor(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['Authorization'] is not None)

            token = data['payload']['Authorization']

            response = issue_prescrtipion(self, token)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully issued.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['id'] is not None)

