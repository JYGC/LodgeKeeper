'''
Documentation
'''
from flask import request, make_response, jsonify, session

from project.server import app
from project.server.models.auth import User

class AuthTokenHelper():
    fail_message = 'Auth token is invalid.'

    def authenticate_request(self):
        """ Function docstring """
        fail_response = None
        if request.path not in app.config.get('EXCLUDE_FROM_AUTHENTICATION'):
            # Do not authenticate options as it doesn't have Authorization
            # header
            if request.method != 'OPTIONS':
                auth_header = request.headers.get('Authorization')
                if isinstance(auth_header, str) and auth_header.startswith(
                        'Bearer'):
                    try:
                        auth_token = auth_header.split(" ")[1]
                        self.decoded_result = User.decode_auth_token(
                            auth_token)
                        if isinstance(self.decoded_result, int
                                ) and self.decoded_result > 0:
                            self.success_action()
                        else:
                            fail_response = make_response(jsonify({
                                'message': self.fail_message
                            })), 401
                    except Exception:
                        fail_response = make_response(jsonify({
                            'message': self.fail_message
                        })), 401
                else:
                    fail_response = make_response(jsonify({
                        'message': self.fail_message
                    })), 401
        return fail_response
    
    def success_action(self):
        """ Action taken  """
        session['user_id'] = self.decoded_result
