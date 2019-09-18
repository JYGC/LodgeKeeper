import json

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
