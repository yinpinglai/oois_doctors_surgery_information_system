import json

from app.test.base import BaseTestCase
from app.main.enum.appointment_type import AppointmentType
from app.main.enum.appointment_status import AppointmentStatus

def login_as_a_receptionist(self):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )),
        content_type='application/json',
    )

def make_an_appointment(self, token: str):
    return self.client.post(
        '/api/appointment/',
        headers=dict(
            Authorization=token,
        ),
        data=json.dumps(dict(
            type=AppointmentType.standard.value,
            patient_id='dad6a212-51e2-4b67-9f95-9c9424500863',
            healthcare_professional_id='00de28e7-73f9-4099-9edc-7d2f3902d7ba',
            start_time='2022-02-12 11:00:00',
            end_time='2022-02-12 12:00:00',
        )),
        content_type='application/json',
    )

def cancel_an_appointment(self, token: str, appointment_id: str):
    return self.client.put(
        f'/api/appointment/{appointment_id}',
        headers=dict(
            Authorization=token,
        ),
        data=json.dumps(dict(
            status=AppointmentStatus.cancelled.value,
        )),
        content_type='application/json',
    )

class TestReceptionist(BaseTestCase):

    def test_can_receptionist_make_an_appointment(self):
        ''' Test for receptionist can make an appointment '''
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

            response = make_an_appointment(self, token)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully booked.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['id'] is not None)


    def test_can_receptionist_cancel_an_appointment(self):
        ''' Test for receptionist can cancel an appointment '''
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

            response = cancel_an_appointment(self, token, appointment_id='b8f74dc8-1b06-40fc-a086-f85d220bf00b')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully updated.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['id'] is not None)

