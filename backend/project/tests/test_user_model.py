# project/tests/test_user_model.py



import unittest

from project.server import db
from project.server.models.auth import Account, User
from project.tests.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_encode_auth_token(self):
        account = Account(
            contact_email='test@test.com',
            contact_address='1488 Tall Dr, Spawnhills, VIC 3532',
            contact_phone='0345464737'
        )
        db.session.add(account)
        db.session.flush()
        user = User(
            email='test@test.com',
            password='test',
            account_id=account.id
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        account = Account(
            contact_email='test@test.com',
            contact_address='1488 Tall Dr, Spawnhills, VIC 3532',
            contact_phone='0345464737'
        )
        db.session.add(account)
        db.session.flush()
        user = User(
            email='test@test.com',
            password='test',
            account_id=account.id
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))

        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8") ) == 1)


if __name__ == '__main__':
    unittest.main()
