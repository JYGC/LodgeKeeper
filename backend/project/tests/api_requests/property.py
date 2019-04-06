''' project/tests/request_functions/auth.py '''


import json


def add_property(self, auth_token, address, property_type):
    ''' add property via api '''
    return self.client.post(
        '/property/add',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        data=json.dumps(dict(address=address, property_type=property_type)),
        content_type='application/json',
    )

def edit_property(self, auth_token, address, property_type, rent_type,
                  description, parking, rent_cost):
    ''' edit property via api '''
    return self.client.post(
        '/property/edit',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        data=json.dumps(dict(address=address, property_type=property_type,
                             rent_type=rent_type, description=description,
                             parking=parking, rent_cost=rent_cost)),
        content_type='application/json',
    )

def get_property(self, auth_token, property_id):
    ''' get property via api '''
    return self.client.post(
        '/property/get',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        data=json.dumps(dict(property_id=property_id)),
        content_type='application/json',
    )

def delete_property(self, auth_token, property_id):
    ''' delete property via api '''
    return self.client.post(
        '/property/delete',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        data=json.dumps(dict(property_id=property_id)),
        content_type='application/json',
    )

def manage_property(self, auth_token):
    ''' get list of properties owned by account via api '''
    return self.client.get(
        '/property',
        headers=dict(
            Authorization='Bearer ' + auth_token
        ),
        content_type='application/json',
    )
