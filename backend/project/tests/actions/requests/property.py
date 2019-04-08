''' project/tests/request_functions/auth.py '''


import json

from project.tests.base import BaseTestCase


def get_property(auth_token, property_id, testcls: BaseTestCase):
    ''' get property via api '''
    return testcls.client.post(
        '/property/get',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        data=json.dumps(dict(property_id=property_id)),
        content_type='application/json',
    )

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

def manage_property(auth_token, testcls: BaseTestCase):
    ''' get list of properties owned by account via api '''
    return testcls.client.get(
        '/property',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        content_type='application/json',
    )
