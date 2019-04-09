''' project/tests/request_functions/auth.py '''


import json

from project.tests.base import BaseTestCase


def delete_property(auth_token, property_id, testcls: BaseTestCase):
    ''' delete property via api '''
    return testcls.client.post(
        '/property/delete',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        data=json.dumps(dict(property_id=property_id)),
        content_type='application/json',
    )
