# project/tests/test_user_model.py



import unittest

from project.server import db
from project.server.models.user import Account, User
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):
    ''' Test methods in user model '''
    test_user_email = 'test@test.com'
    test_user_address = '1488 Tall Dr, Spawnhills, VIC 3532'
    test_user_phone = '0345464737'
    test_user_password = 'test'

    def test_encode_auth_token(self):
        account = Account(
            contact_email=self.test_user_email,
            contact_address=self.test_user_address,
            contact_phone=self.test_user_phone
        )
        db.session.add(account)
        db.session.flush()
        user = User(
            email=self.test_user_email,
            password=self.test_user_password,
            account_id=account.id
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        account = Account(
            contact_email=self.test_user_email,
            contact_address=self.test_user_address,
            contact_phone=self.test_user_phone
        )
        db.session.add(account)
        db.session.flush()
        user = User(
            email=self.test_user_email,
            password=self.test_user_password,
            account_id=account.id
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8")) == 1)


if __name__ == '__main__':
    unittest.main()
