from abc import ABC, abstractmethod

from project.tests.base import BaseTestCase
from project.tests.values.auth_values import UserValues

class ActionABC(ABC):
    def __init__(self, test_cls: BaseTestCase):
        self.test_cls = test_cls

    @abstractmethod
    def run(self, test_values):
        ...

class ApiCheckActionABC(ABC):
    @abstractmethod
    def api_request(self, test_values):
        ...

    @abstractmethod
    def check_response(self, data, resp):
        ...

class DBCheckActionABC(ABC):
    @abstractmethod
    def check_db_state(self, test_values, data):
        ...