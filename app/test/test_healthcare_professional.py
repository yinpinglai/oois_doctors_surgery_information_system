import json

from app.test.base import BaseTestCase
from app.main.enum.appointment_status import AppointmentStatus

def login_as_a_doctor(self):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='kenny.law@gmail.com',
            password='P@ssw0rd',
        )),
        content_type='application/json',
    )

def login_as_a_nurse(self):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='james.lam@gmail.com',
            password='P@ssw0rd',
        )),
        content_type='application/json',
    )

def perform_consulting_service(self, token: str, appointment_id: str):
    return self.client.put(
        f'/api/appointment/{appointment_id}',
        headers=dict(
            Authorization=token,
        ),
        data=json.dumps(dict(
            status=AppointmentStatus.consulting.value,
        )),
        content_type='application/json',
    )


class TestHealthcareProfessional(BaseTestCase):

    def test_perform_consulting_service_by_doctors(self):
        ''' Test for doctors can perform consulting services for patients '''
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

            response = perform_consulting_service(self, token, appointment_id='b8f74dc8-1b06-40fc-a086-f85d220bf00b')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully updated.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['id'] is not None)


    def test_perform_consulting_service_by_nurses(self):
        ''' Test for nurses can perform consulting services for patients '''
        with self.client:
            response = login_as_a_nurse(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully logged in.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['Authorization'] is not None)

            token = data['payload']['Authorization']

            response = perform_consulting_service(self, token, appointment_id='5a08be2e-269d-42cf-8867-bee3b20ced90')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully updated.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['id'] is not None)

