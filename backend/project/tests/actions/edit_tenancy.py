import json

from project.tests.actions.response_handling import ChkSuccessfulModelResponse


class EditTenancyApi():
    @staticmethod
    def run(test_cls, tenancy_test_value, tenancy_id_test_value, auth_token):
        return test_cls.client.post(
            '/tenancy/edit',
            headers=dict(Authorization='Bearer ' + auth_token),
            data=json.dumps(dict(tenancy_test_value,
                                 tenancy_id=tenancy_id_test_value)),
            content_type='application/json',
        )

class ChkEditTenancyResponse(ChkSuccessfulModelResponse):
    _id_key = 'tenancy_id'
    _resp_code = 200
