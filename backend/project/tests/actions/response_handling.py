import json


class ChkSuccessfulJsonResponse():
    _status_value = 'success'
    _resp_code = 0

    @classmethod
    def run(self, test_cls, response):
        data = json.loads(response.data.decode())
        test_cls.assertEqual(data['status'], self._status_value)
        self.extract_data(test_cls, data)
        test_cls.assertEqual(response.content_type, 'application/json')
        test_cls.assertEqual(response.status_code, self._resp_code)

    @classmethod
    def extract_data(self, test_cls, data):
        pass


class ChkSuccessfulMsgResponse(ChkSuccessfulJsonResponse):
    _msg_key = 'message'
    _msg_value = None

    @classmethod
    def extract_data(self, test_cls, data):
        test_cls.assertEqual(data[self._msg_key], self._msg_value)


class ChkFailedMsgResponse(ChkSuccessfulMsgResponse):
    _status_value = 'fail'


class ChkSuccessfulAuthResponse(ChkSuccessfulMsgResponse):
    _auth_key = None

    @classmethod
    def extract_data(self, test_cls, data):
        super().extract_data(test_cls, data)
        test_cls.assertTrue(data[self._auth_key])


class ChkSuccessfulModelResponse(ChkSuccessfulJsonResponse):
    _id_key = None

    @classmethod
    def extract_data(self, test_cls, data):
        test_cls.assertIn('d', data)
        test_cls.assertTrue(data['d'][self._id_key])


class ChkResponseActionInvaildToken():
    @staticmethod
    def run(test_cls, response):
        data = json.loads(response.data.decode())
        test_cls.assertEqual(data['status'], 'fail')
        test_cls.assertNotIn('d', data)
        test_cls.assertEqual(data['message'],
                             'Invalid token. Please log in again.')
        test_cls.assertEqual(response.content_type,
                             'application/json')
        test_cls.assertEqual(response.status_code, 401)


class ChkResponseActionBadRequest():
    @staticmethod
    def run(test_cls, response):
        data = json.loads(response.data.decode())
        test_cls.assertEqual(data['status'], 'fail')
        test_cls.assertEqual(response.content_type,
                             'application/json')
        test_cls.assertEqual(response.status_code, 400)


def get_d_value(response, value_name):
    return json.loads(response.data.decode())['d'][value_name]