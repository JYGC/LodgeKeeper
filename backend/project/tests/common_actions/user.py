import json

from project.tests.api_requests.auth import login_user, register_user


def register_and_login_user(self):
    ''' Normal user registration and login '''
    # user registration
    resp_register = register_user(self, self.test_user_email,
                                  self.test_user_password,
                                  self.test_user_address,
                                  self.test_user_phone)
    data_register = json.loads(resp_register.data.decode())
    self.assertTrue(data_register['status'] == 'success')
    self.assertTrue(
        data_register['message'] == 'Successfully registered.'
    )
    self.assertTrue(data_register['auth_token'])
    self.assertTrue(resp_register.content_type == 'application/json')
    self.assertEqual(resp_register.status_code, 201)
    # user login
    resp_login = login_user(self, self.test_user_email,
                            self.test_user_password)
    data_login = json.loads(resp_login.data.decode())
    self.assertTrue(data_login['status'] == 'success')
    self.assertTrue(data_login['message'] == 'Successfully logged in.')
    self.assertTrue(data_login['auth_token'])
    self.assertTrue(resp_login.content_type == 'application/json')
    self.assertEqual(resp_login.status_code, 200)
    return data_login
