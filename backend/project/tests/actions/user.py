import json
from typing import Union

from project.tests.base import BaseTestCase
from project.tests.actions.abcs import (ActionABC, ApiCheckActionABC,
                                        DBCheckActionABC)
from project.tests.values.auth_values import UserValues

class RegisterUser(ActionABC, ApiCheckActionABC, DBCheckActionABC):
    ''' Perform test user registration'''
    test_cls = None

    def __init__(self, test_cls: BaseTestCase):
        self.test_cls = test_cls

    def api_request(self, test_values: UserValues):
        ''' register user via api '''
        return self.test_cls.client.post(
            '/auth/register',
            data=json.dumps(dict(email=test_values.email,
                                 password=test_values.password,
                                 address=test_values.address,
                                 phone=test_values.phone)),
            content_type='application/json',
        )
    
    def run(self, test_values: UserValues):
        ''' run action '''
        resp_register = self.api_request(test_values)
        data_register = json.loads(resp_register.data.decode())
        self.check_response(resp_register, data_register)
        return data_register

    def check_response(self, resp, data):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertEqual(data['message'], 'Successfully registered.')
        self.test_cls.assertTrue(data['auth_token'])
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 201)
    
    def check_db_state(self):
        pass


class RegisterDuplicateUser(RegisterUser):
    ''' Try to regsiter user that already exist '''
    def check_response(self, resp, data):
            self.test_cls.assertEqual(data['status'], 'fail')
            self.test_cls.assertEqual(data['message'],
                                      'User already exists. Please Log in.')
            self.test_cls.assertEqual(resp.content_type, 'application/json')
            self.test_cls.assertEqual(resp.status_code, 202)


class LoginUser(ActionABC, ApiCheckActionABC, DBCheckActionABC):
    ''' Perform test user login'''
    test_cls = None

    def __init__(self, test_cls: BaseTestCase):
        self.test_cls = test_cls

    def api_request(self, test_values: UserValues):
        ''' login user via api '''
        return self.test_cls.client.post(
            '/auth/login',
            data=json.dumps(dict(email=test_values.email,
                                 password=test_values.password)),
            content_type='application/json',
        )

    def run(self, test_values: UserValues):
        ''' run action '''
        resp_login = self.api_request(test_values)
        data_login = json.loads(resp_login.data.decode())
        self.check_response(resp_login, data_login)
        return data_login

    def check_response(self, resp, data):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertEqual(data['message'],'Successfully logged in.')
        self.test_cls.assertTrue(data['auth_token'])
        self.test_cls.assertTrue(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 200)
    
    def check_db_state(self):
        pass

class LoginNonExistingUser(LoginUser):
    ''' Try logging in with non-existent user '''
    def check_response(self, resp, data):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertEqual(data['message'], 'User does not exist.')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 404)