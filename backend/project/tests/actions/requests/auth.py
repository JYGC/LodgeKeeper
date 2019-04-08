''' project/tests/actions/requests/auth.py '''


import json


def register_user(self, email, password, address, phone):
    ''' register user via api '''
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(email=email, password=password, address=address,
                             phone=phone)),
        content_type='application/json',
    )

def login_user(self, email, password):
    ''' login user via api '''
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(email=email, password=password)),
        content_type='application/json',
    )
