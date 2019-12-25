import json

from project.tests.actions.response_handling import (ChkSuccessfulMsgResponse,
                                                     ChkFailedMsgResponse)


class LogoutUserApiAction():
    @staticmethod
    def run(test_cls, resp_login):
        return test_cls.client.get(
            '/user/logout',
            headers=dict(
                Authorization='Bearer ' + json.loads(
                    resp_login.data.decode()
                )['auth_token']
            )
        )


class ChkLogoutUserRespAction(ChkSuccessfulMsgResponse):
    _msg_value = 'Successfully logged out.'
    _resp_code = 200


class ChkExpiredLogoutRespAction(ChkFailedMsgResponse):
    _msg_value = 'Signature expired. Please log in again.'
    _resp_code = 401


class ChkBlacklistLogoutRespAction(ChkFailedMsgResponse):
    _msg_value = 'Token blacklisted. Please log in again.'
    _resp_code = 401
