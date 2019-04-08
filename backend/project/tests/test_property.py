''' project/tests/test_property.py '''


import json, unittest, random, string

from project.server import db
from project.server.models.property import Property, PropertyType
from project.tests.base import BaseTestCase
from project.tests.actions.user import RegisterUser
from project.tests.actions.property import (AddProperty, AddPropertyBadToken,
                                            EditProperty, EditPropertyBadToken)
from project.tests.values.auth_values import UserValues
from project.tests.values.property_values import PropertyValues


class TestPropertyBlueprint(BaseTestCase):
    ''' Test views in Property Blueprint '''
    test_user_values = UserValues()
    test_user_values.email = 'freedom@bix.com'
    test_user_values.password = 'Test3r$'
    test_user_values.address = '130 Fake Street, Homeburg, VIC 6969'
    test_user_values.phone = '0456758474'

    test_property_values = PropertyValues()
    test_property_values.property_address = 'Unit 56, 345 Fawkes Street, North Balk, NSW 3222'
    test_property_values.property_type = 'Landed Property'
    test_property_values.rent_type = 'Whole Property'
    test_property_values.description = 'Description 1'
    test_property_values.parking = False
    test_property_values.rent_cost = 456.22

    test_property_values_2 = PropertyValues()
    test_property_values_2.property_address = 'Unit 45, 345 Faes Drive, North Balk, NSW 3222',
    test_property_values_2.property_type = 'Apartment',
    test_property_values_2.rent_type = 'Private Room',
    test_property_values_2.description = 'Description 2',
    test_property_values_2.parking = True,
    test_property_values_2.rent_cost = 650.09

    test_property_values_3 = PropertyValues()
    test_property_values_3.property_address = '345 Unit Street, North Balk, NSW 3222',
    test_property_values_3.property_type = 'Landed Property',
    test_property_values_3.rent_type = 'Private Room',
    test_property_values_3.description = 'Description 3',
    test_property_values_3.parking = True,
    test_property_values_3.rent_cost = 1000.05

    test_fake_token = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))

    def setup_actions(self):
        ''' Initialize Action objects '''
        self.user_register = RegisterUser(self)
        self.add_property = AddProperty(self)
        self.add_property_bad_token = AddPropertyBadToken(self)
        self.edit_property = EditProperty(self)
        self.edit_property_bad_token = EditPropertyBadToken(self)

    def test_add_property(self):
        ''' Test adding new property '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            self.add_property.run(data_user['auth_token'],
                                  self.test_property_values)

    def test_add_property_with_invalid_token(self):
        ''' Test adding new property with invalid token '''
        with self.client:
            self.user_register.run(self.test_user_values)
            self.add_property_bad_token.run(self.test_fake_token,
                                            self.test_property_values)

    def test_edit_property_first_time(self):
        ''' Test editing property for the first time '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.edit_property.run(data_user['auth_token'],
                                   data_property['property_id'],
                                   self.test_property_values)

    def test_edit_property(self):
        ''' Test editing property '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.edit_property.run(data_user['auth_token'],
                                   data_property['property_id'],
                                   self.test_property_values)
            self.edit_property.run(data_user['auth_token'],
                                   data_property['property_id'],
                                   self.test_property_values_2)

    def test_edit_property_with_invalid_token(self):
        ''' Test editing property with invalid token '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.edit_property_bad_token.run(data_user['auth_token'],
                                   data_property['property_id'],
                                   self.test_property_values)

    def test_get_property(self):
        ''' Test getting property data '''
        self.assertTrue(False)

    def test_get_property_with_invalid_token(self):
        ''' Test getting property with invalid token '''
        self.assertTrue(False)

    def test_list_property_with_no_property(self):
        ''' Test list property with account that has no property '''
        self.assertTrue(False)

    def test_list_property_after_add(self):
        ''' Test list property after adding properties '''
        self.assertTrue(False)

    def test_list_property_after_add_edit(self):
        ''' Test list property after adding and editing properties '''
        self.assertTrue(False)

    def test_list_property_after_add_edit_delete(self):
        ''' Test list property after adding, editing and deleting properties '''
        self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()