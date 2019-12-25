import json

from project.tests.base import BaseTestCase
from project.tests.actions.response_handling import (ChkSuccessfulAuthResponse,
                                                     ChkFailedMsgResponse)


class RegisterUserApiAction():
    @staticmethod
    def run(test_cls, user_values):
        ''' register user via api '''
        return test_cls.client.post(
            '/user/register',
            data=json.dumps(dict(email=user_values['email'],
                                 password=user_values['password'],
                                 address=user_values['address'],
                                 phone=user_values['phone'])),
            content_type='application/json',
        )


class ChkRegUserRespAction(ChkSuccessfulAuthResponse):
    _resp_code = 201
    _auth_key = 'auth_token'
    _msg_value = 'Successfully registered.'


class ChkRegExistingUserRespAction(ChkFailedMsgResponse):
    _resp_code = 202
    _msg_value = 'User already exists. Please Log in.'


class RegisterUserHelper():
    @staticmethod
    def register_user_get_auth_token(test_cls, user_values):
        return json.loads(RegisterUserApiAction.run(
            test_cls,
            user_values
        ).data.decode())['auth_token']
