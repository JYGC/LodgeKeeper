import json

from project.tests.base import BaseTestCase
from project.tests.actions.abcs import (IAction, IApiCheckAction,
                                        IDbCheckAction)


class AddTenancy(IAction, IApiCheckAction, IDbCheckAction):
    ''' Add new tenancy '''
    def __init__(self, test_cls: BaseTestCase):
        super().__init__(test_cls)
    
    # def api_request(self, auth_token, test_values: TenancyValues):
    #     ''' add tenancy via api '''
    #     return self.test_cls.client.post(
    #         '/tenancy/add',
    #         headers=dict(Authorization='Bearer ' + auth_token),
    #         data=json.dumps(dict(

    #         ))
    #     )
