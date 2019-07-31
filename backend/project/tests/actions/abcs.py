from project.tests.base import BaseTestCase
from project.tests.values.auth_values import UserValues


class IAction():
    def __init__(self, test_cls: BaseTestCase):
        self.test_cls = test_cls

    def run(self, test_values):
        pass


class IApiCheckAction():
    def api_request(self, test_values):
        pass

    def check_response(self, data, resp):
        pass


class IDbCheckAction():
    def check_db_state(self, test_values, data):
        pass
