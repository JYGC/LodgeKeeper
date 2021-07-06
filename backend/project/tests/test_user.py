'''
project/tests/test_auth.py
'''


import time
import json
import unittest

from project.server import db
from project.server.models.user import Account, User, BlacklistToken
from project.tests.base import BaseTestCase
from project.tests.actions.register_user import (RegisterUserApiAction,
                                                 ChkRegUserRespAction,
                                                 ChkRegExistingUserRespAction)
from project.tests.actions.login_user import (LoginUserApiAction,
                                              ChkLoginUserRespAction,
                                              ChkLoginNonExistingUser)
from project.tests.actions.logout_user import (LogoutUserApiAction,
                                               ChkLogoutUserRespAction,
                                               ChkExpiredLogoutRespAction,
                                               ChkBlacklistLogoutRespAction)
from project.tests.actions.user_db_check import ChkOneUserInDb
from project.tests.actions.requests.auth import login_user, register_user
from project.tests.actions.auth_user import (AuthUserApiAction,
                                             AuthUserApiActionMalToken,
                                             ChkSuccessUserAuth,
                                             ChkBadTokenUserAuth,
                                             ChkBlackListTokenUserAuth)
from project.tests.values import user_values


class TestRegisterUserAPI(BaseTestCase):
    ''' Test views in User Blueprint '''

    def test_registration(self):
        """ Test for user registration """
        with self.client:
            resp_reguser = RegisterUserApiAction.run(self, user_values.USER_1)
            ChkRegUserRespAction.run(self, resp_reguser)
            ChkOneUserInDb.run(self, user_values.USER_1)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email"""
        with self.client:
            RegisterUserApiAction.run(self, user_values.USER_1)
            resp_reguser = RegisterUserApiAction.run(self, user_values.USER_1)
            ChkRegExistingUserRespAction.run(self, resp_reguser)
            ChkOneUserInDb.run(self, user_values.USER_1)


class TestLoginUserAPI(BaseTestCase):
    def test_registered_user_login(self):
        """ Test for login of registered-user login """
        with self.client:
            RegisterUserApiAction.run(self, user_values.USER_1)
            resp_loginuser = LoginUserApiAction.run(self, user_values.USER_1)
            ChkLoginUserRespAction.run(self, resp_loginuser)

    def test_non_registered_user_login(self):
        """ Test for login of user that does not exist """
        with self.client:
            resp_loginuser = LoginUserApiAction.run(self, user_values.USER_1)
            ChkLoginNonExistingUser.run(self, resp_loginuser)


class TestUserStatusAPI(BaseTestCase):
    def test_user_status(self):
        """ Test for user status """
        with self.client:
            resp_reguser = RegisterUserApiAction.run(self, user_values.USER_1)
            resp_userauth = AuthUserApiAction.run(self, resp_reguser)
            ChkSuccessUserAuth.run(self, user_values.USER_1, resp_userauth)

    def test_user_status_malformed_bearer_token(self):
        """ Test for user status with malformed bearer token """
        with self.client:
            resp_reguser = RegisterUserApiAction.run(self, user_values.USER_1)
            resp_userauth = AuthUserApiActionMalToken.run(self, resp_reguser)
            ChkBadTokenUserAuth.run(self, user_values.USER_1, resp_userauth)

    def test_valid_blacklisted_token_user(self):
        """ Test for user status with a blacklisted valid token """
        with self.client:
            resp_reguser = RegisterUserApiAction.run(self, user_values.USER_1)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_reguser.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            resp_userauth = AuthUserApiAction.run(self, resp_reguser)
            ChkBlackListTokenUserAuth.run(self, user_values.USER_1,
                                          resp_userauth)


class TestLogoutUserAPI(BaseTestCase):
    def test_valid_logout(self):
        """ Test for logout before token expires """
        with self.client:
            resp_reguser = RegisterUserApiAction.run(self, user_values.USER_1)
            resp_userauth = AuthUserApiAction.run(self, resp_reguser)
            ChkSuccessUserAuth.run(self, user_values.USER_1, resp_userauth)
            resp_logoutuser = LogoutUserApiAction.run(self, resp_reguser)
            ChkLogoutUserRespAction.run(self, resp_logoutuser)

    def test_invalid_logout(self):
        """ Testing logout after the token expires """
        with self.client:
            # test login expiration after registering
            resp_reguser = RegisterUserApiAction.run(self, user_values.USER_1)
            ChkRegUserRespAction.run(self, resp_reguser)
            time.sleep(6)
            resp_logoutuser = LogoutUserApiAction.run(self, resp_reguser)
            ChkExpiredLogoutRespAction.run(self, resp_logoutuser)
            # test login expiration after login
            resp_loginuser = LoginUserApiAction.run(self, user_values.USER_1)
            ChkLoginUserRespAction.run(self, resp_loginuser)
            time.sleep(6)
            resp_logoutuser = LogoutUserApiAction.run(self, resp_reguser)
            ChkExpiredLogoutRespAction.run(self, resp_logoutuser)

    def test_valid_blacklisted_token_logout(self):
        """ Test for logout after a valid token gets blacklisted """
        with self.client:
            RegisterUserApiAction.run(self, user_values.USER_1)
            resp_loginuser = LoginUserApiAction.run(self, user_values.USER_1)
            ChkLoginUserRespAction.run(self, resp_loginuser)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_loginuser.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            resp_logoutuser = LogoutUserApiAction.run(self, resp_loginuser)
            ChkBlacklistLogoutRespAction.run(self, resp_logoutuser)


if __name__ == '__main__':
    unittest.main()
