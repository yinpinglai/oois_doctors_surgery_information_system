import json
import datetime

from app.test.base import BaseTestCase

def login_as_a_receptionist(self):
    return self.client.post(
        '/api/auth/login',
        data=json.dumps(dict(
            email='kris.lai@gmail.com',
            password='P@ssw0rd',
        )),
        content_type='application/json',
    )

def get_next_available(self, token: str, healthcare_professional_id: str):
    now = datetime.datetime.now()
    date_time_format = '%Y-%m-%d %H:%M:%S'
    start_time = (now - datetime.timedelta(
        hours=now.hour,
        minutes=now.minute,
        seconds=now.second,
    ) + datetime.timedelta(hours=1)).strftime(date_time_format)
    end_time = (now - datetime.timedelta(
        hours=now.hour,
        minutes=now.minute,
        seconds=now.second,
    ) + datetime.timedelta(hours=9)).strftime(date_time_format)
    return self.client.get(
        f'/api/appointment/next-available?healthcare_professional_id={healthcare_professional_id}&start_time={start_time}&end_time={end_time}',
        headers=dict(
            Authorization=token,
        ),
    )

class TestAppointmentSchedule(BaseTestCase):

    def test_get_next_available_time_slot_for_a_healthcare_professional(self):
        ''' Test for getting the next available time slot for a healthcare professional '''
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

            response = get_next_available(self, token, healthcare_professional_id='67efe526-0bd0-43b9-8d0c-63ff104fcefa')
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['is_success'] == True)
            self.assertTrue(data['message'] == 'Successfully fetched.')
            self.assertTrue(data['payload'] is not None)
            self.assertTrue(data['payload']['start_time'] is not None)
            self.assertTrue(data['payload']['end_time'] is not None)

