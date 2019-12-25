import json

from project.tests.actions.response_handling import (
    ChkSuccessfulAuthResponse,
    ChkFailedMsgResponse
)

class LoginUserApiAction():
    @staticmethod
    def run(test_cls, user_values):
        ''' login user via api '''
        return test_cls.client.post(
            '/user/login',
            data=json.dumps(dict(email=user_values['email'],
                                 password=user_values['password'])),
            content_type='application/json',
        )


class ChkLoginUserRespAction(ChkSuccessfulAuthResponse):
    _resp_code = 200
    _auth_key = 'auth_token'
    _msg_value = 'Successfully logged in.'


class ChkLoginNonExistingUser(ChkFailedMsgResponse):
    _resp_code = 404
    _msg_value = 'User does not exist.'
