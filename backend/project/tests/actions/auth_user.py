import json

class AuthUserApiAction():
    _bearer_label = 'Bearer '

    @classmethod
    def run(self, test_cls, resp):
        ''' authenicate user via api '''
        return test_cls.client.get(
            '/user/auth',
            headers=dict(
                Authorization=self._bearer_label + json.loads(
                    resp.data.decode()
                )['auth_token']
            )
        )
    

class AuthUserApiActionMalToken(AuthUserApiAction):
    _bearer_label = 'Bearer'


class ChkUserAuth():
    _status_value = None
    _resp_code = 0

    @classmethod
    def run(self, test_cls, user_values, resp):
        data = json.loads(resp.data.decode())
        test_cls.assertEqual(data['status'], self._status_value)
        self._handle_data(test_cls, user_values, data)
        test_cls.assertEqual(resp.status_code, self._resp_code)
    
    @classmethod
    def _handle_data(self, test_cls, user_values, data):
        None


class ChkSuccessUserAuth(ChkUserAuth):
    _status_value = 'success'
    _resp_code = 200

    @classmethod
    def _handle_data(self, test_cls, user_values, data):
        test_cls.assertIsNotNone(data['d'])
        test_cls.assertEqual(data['d']['email'], user_values['email'])


class ChkBadTokenUserAuth(ChkUserAuth):
    _status_value = 'fail'
    _resp_code = 401
    
    @classmethod
    def _handle_data(self, test_cls, user_values, data):
        test_cls.assertEqual(data['message'], 'Bearer token malformed.')


class ChkBlackListTokenUserAuth(ChkUserAuth):
    _status_value = 'fail'
    _resp_code = 401
    
    @classmethod
    def _handle_data(self, test_cls, user_values, data):
        test_cls.assertEqual(data['message'],
                             'Token blacklisted. Please log in again.')
