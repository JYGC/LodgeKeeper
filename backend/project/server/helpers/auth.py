'''
Documentation
'''
from flask import request, make_response, jsonify, session

from project.server import app
from project.server.models.auth import User

class AuthTokenValidator():
    ''' Auth Token Validator '''
    auth_token = None
    decoded_result = None

    auth_err_msg = 'Authentication failed.'
    valid_token_err_msg = 'Provide a valid auth token.'
    malformed_token_err_msg = 'Bearer token malformed.'
    unknown_err_msg = 'Unknown authentication failure.'

    def testing_err_msg(self, testing_err_msg):
        '''
        Use more specific messages in unit testing to make it easier to debug an
        issue.
        '''
        return testing_err_msg if app.config['TESTING'] else self.auth_err_msg

    def validate(self):
        ''' Function docstring '''
        if request.path in app.config.get(
                'EXCLUDE_FROM_AUTHENTICATION') or request.method == 'OPTIONS':
            # Do not authenticate HTTP OPTIONS as it doesn't have Authorization
            # header and do not validate paths like login or register
            return None

        auth_header = request.headers.get('Authorization')
        if not isinstance(auth_header, str) or not auth_header.startswith(
                'Bearer '):
            return make_response(jsonify({
                'status': 'fail',
                'message': self.testing_err_msg(self.malformed_token_err_msg)
            })), 401

        try:
            self.auth_token = auth_header.split(" ")[1]
            self.decoded_result = User.decode_auth_token(self.auth_token)
            if isinstance(self.decoded_result, int) and self.decoded_result > 0:
                session['user_id'] = self.decoded_result
                session['auth_token'] = self.auth_token
                # Successful authentication
                return None
            return make_response(jsonify({
                'status': 'fail',
                'message': self.testing_err_msg(self.decoded_result)
            })), 401
        except (IndexError, AttributeError):
            return make_response(jsonify({
                'status': 'fail',
                'message': self.testing_err_msg(self.valid_token_err_msg)
            })), 401

        return make_response(jsonify({
            'status': 'fail',
            'message': self.testing_err_msg(self.unknown_err_msg)
        })), 401
