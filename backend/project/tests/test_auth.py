'''
project/tests/test_auth.py
'''


import time, json, unittest, random, string

from project.server import db
from project.server.models.auth import Account, User, BlacklistToken
from project.tests.base import BaseTestCase
from project.tests.values.auth_values import UserValues
from project.tests.actions.user import (RegisterUser, RegisterDuplicateUser,
                                        LoginUser, LoginNonExistingUser)
from project.tests.actions.requests.auth import login_user, register_user


class TestAuthBlueprint(BaseTestCase):
    ''' Test views in Auth Blueprint '''
    test_user_values = UserValues() # Needs work (continute later)
    test_user_email = test_user_values.email = 'joe@gmail.com'
    test_user_password = test_user_values.password = 'Test3r$'
    test_user_password2 = test_user_values.password2 = 'f15her$'
    test_user_address = test_user_values.address = '130 Fake Street, Homeburg, VIC 6969'
    test_user_phone = test_user_values.phone = '0456758474'

    test_fake_token = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))

    def setup_actions(self):
        ''' Initialize Action objects '''
        self.register_user = RegisterUser(self)
        self.register_duplicate_user = RegisterDuplicateUser(self)
        self.login_user = LoginUser(self)
        self.login_nonexistent_user = LoginNonExistingUser(self)

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            self.register_user.run(self.test_user_values)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        account = Account(contact_email=self.test_user_email,
                          contact_address=self.test_user_address,
                          contact_phone=self.test_user_phone)
        db.session.add(account)
        db.session.flush()
        user = User(email=self.test_user_email,
                    password=self.test_user_password2, account_id=account.id)
        db.session.add(user)
        db.session.commit()
        with self.client:
            self.register_duplicate_user.run(self.test_user_values)

    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            self.register_user.run(self.test_user_values)
            self.login_user.run(self.test_user_values)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            self.login_nonexistent_user.run(self.test_user_values)

    def test_user_status(self):
        """ Test for user status """
        with self.client:
            resp_register = register_user(self, self.test_user_email,
                                          self.test_user_password,
                                          self.test_user_address,
                                          self.test_user_phone)
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == self.test_user_email)
            self.assertTrue(str(data['data']['admin']) == 'True' or 'False')
            self.assertEqual(response.status_code, 200)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token """
        with self.client:
            resp_register = register_user(self, self.test_user_email,
                                          self.test_user_password,
                                          self.test_user_address,
                                          self.test_user_phone)
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Bearer token malformed.')
            self.assertEqual(response.status_code, 401)

    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            # user registration
            resp_register = register_user(self, self.test_user_email,
                                          self.test_user_password,
                                          self.test_user_address,
                                          self.test_user_phone)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
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
            # valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully logged out.')
            self.assertEqual(response.status_code, 200)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # user registration
            resp_register = register_user(self, self.test_user_email,
                                          self.test_user_password,
                                          self.test_user_address,
                                          self.test_user_phone)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
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
            # invalid token logout
            time.sleep(6)
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            resp_register = register_user(self, self.test_user_email,
                                          self.test_user_password,
                                          self.test_user_address,
                                          self.test_user_phone)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.')
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
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_login.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_login.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        """ Test for user status with a blacklisted valid token """
        with self.client:
            resp_register = register_user(self, self.test_user_email,
                                          self.test_user_password,
                                          self.test_user_address,
                                          self.test_user_phone)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_register.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
