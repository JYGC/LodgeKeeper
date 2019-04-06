''' project/tests/test_property.py '''


import json, unittest, random, string

from project.server import db
from project.server.models.property import Property
from project.tests.base import BaseTestCase
from project.tests.api_requests.auth import login_user, register_user
from project.tests.api_requests.property import (add_property, delete_property,
                                                 edit_property, get_property)
from project.tests.common_actions.user import register_and_login_user


class TestPropertyBlueprint(BaseTestCase):
    ''' Test views in Property Blueprint '''
    test_user_email = 'freedom@bix.com'
    test_user_password = 'Test3r$'
    test_user_address = '130 Fake Street, Homeburg, VIC 6969'
    test_user_phone = '0456758474'
    test_property_address = 'Unit 56, 345 Fawkes Street, North Balk, NSW 3222'
    test_property_type = 'Landed Property'
    test_fake_token = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))

    def test_add_property(self):
        ''' Test adding new property '''
        with self.client:
            data_user = register_and_login_user(self)
            # add new property
            resp_property = add_property(self, data_user['auth_token'],
                                         self.test_user_address,
                                         self.test_property_type)
            # check response add new property
            data_property = json.loads(resp_property.data.decode())
            self.assertTrue(data_property['status'] == 'success')
            self.assertTrue(resp_property.content_type == 'application/json')
            self.assertEqual(resp_property.status_code, 201)

    def test_add_property_with_invalid_token(self):
        ''' Test adding new property with invalid token '''
        register_and_login_user(self)
        # add new property
        resp_property = add_property(self, self.test_fake_token,
                                     self.test_user_address,
                                     self.test_property_type)
        # check response add new property
        data_property = json.loads(resp_property.data.decode())
        self.assertTrue(data_property['status'] == 'fail')
        self.assertTrue(data_property[
            'message'] == 'Invalid token. Please log in again.')
        self.assertTrue(resp_property.content_type == 'application/json')
        self.assertEqual(resp_property.status_code, 401)

    def test_edit_property(self):
        ''' Test adding new property '''
            # user registration
            # check response user registration
            # user login
            # check response user login
            # get auth token
            # add property
            # check add property
            # edit property
            # check edit property

    def test_edit_property_with_invalid_token(self):
        ''' Test adding new property '''
            # user registration
            # check response user registration
            # user login
            # check response user login
            # make fake auth token
            # edit new property
            # check response edit property

    def test_list_property_with_no_property(self):
        ''' Test list property with account that has no property '''

    def test_list_property_after_add(self):
        ''' Test list property after adding properties '''

    def test_list_property_after_add_edit(self):
        ''' Test list property after adding and editing properties '''

    def test_list_property_after_add_edit_delete(self):
        ''' Test list property after adding, editing and deleting properties '''


if __name__ == '__main__':
    unittest.main()