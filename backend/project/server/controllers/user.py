'''
Blueprint for all controllers facilitating user account related functionality
'''


from flask import Blueprint, request, make_response, jsonify, session
from flask.views import MethodView

from project.server import bcrypt, db
from project.server.models.auth import Account, User, BlacklistToken

user_blueprint = Blueprint('user', __name__)


class RegisterAPI(MethodView):
    ''' User Registration Resource '''

    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                account = Account(
                    contact_email=post_data.get('email'),
                    contact_address=post_data.get('address'),
                    contact_phone=post_data.get('phone')
                )
                # insert new account and flush changes to get this id
                db.session.add(account)
                db.session.flush()
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    account_id=account.id
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                response = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(response)), 201
            except Exception:
                response = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(response)), 401
        else:
            response = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(response)), 202


class LoginAPI(MethodView):
    ''' User Login Resource '''
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(email=post_data.get('email')).first()
            if user and bcrypt.check_password_hash(user.password,
                                                   post_data.get('password')):
                auth_token = user.encode_auth_token(user.id)
                #session['auth_token'] = auth_token
                if auth_token:
                    response = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(response)), 200
            else:
                response = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(response)), 404
        except Exception as ex:
            response = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(response)), 500


class UserAPI(MethodView):
    ''' User Resource '''
    def get(self):
        # Auth user
        user_id = session.pop('user_id', None)
        user = User.query.filter_by(id=int(user_id)).first()
        return make_response(jsonify({
            'status': 'success',
            'd': {
                'user_id': user.id,
                'email': user.email,
                'admin': user.admin,
                'registered_on': user.registered_on
            }
        })), 200


class LogoutAPI(MethodView):
    ''' Logout Resource '''
    def get(self):
        response = None
        try:
            auth_token = session.pop('auth_token', None)
            blacklist_token = BlacklistToken(token=auth_token)
            db.session.add(blacklist_token)
            db.session.commit()
            response = {
                'status': 'success',
                'message': 'Successfully logged out.'
            }
            response = make_response(jsonify(response)), 200
        except Exception:
            response = {
                'status': 'fail',
                'message': 'Failed to logout'
            }
            response = make_response(jsonify(response)), 401
        return response

# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
user_blueprint.add_url_rule(
    '/user/register',
    view_func=registration_view,
    methods=['POST']
)
user_blueprint.add_url_rule(
    '/user/login',
    view_func=login_view,
    methods=['POST']
)
user_blueprint.add_url_rule(
    '/user/auth',
    view_func=user_view,
    methods=['GET']
)
user_blueprint.add_url_rule(
    '/user/logout',
    view_func=logout_view,
    methods=['GET']
)
