''' project/tests/test_property.py '''


import unittest
import random
import string

from project.tests.base import BaseTestCase
from project.tests.actions.user import RegisterUser
from project.tests.actions.property import (AddProperty, AddPropertyBadToken,
                                            EditProperty, EditPropertyBadToken,
                                            EditNonexistentProperty,
                                            GetProperty, GetNonexistentProperty,
                                            GetPropertyBadToken, ListProperty,
                                            ListPropertyNoProperty,
                                            DeleteProperty,
                                            DeleteNonexistentProperty)
from project.tests.values.auth_values import UserValues
from project.tests.values.property_values import PropertyValues


class TestPropertyBlueprint(BaseTestCase):
    ''' Test views in Property Blueprint '''
    test_user_values = UserValues()
    test_user_values.email = 'freedom@bix.com'
    test_user_values.password = 'Test3r$'
    test_user_values.address = '130 Fake Street, Homeburg, VIC 6969'
    test_user_values.phone = '0456758474'

    test_user_values_2 = UserValues()
    test_user_values_2.email = 'gavin.manspreader@hotmail.com'
    test_user_values_2.password = 'Fa$t5'
    test_user_values_2.address = '99 Golburn Street, Holmeshill, VIC 3333'
    test_user_values_2.phone = '0456758474'

    test_property_values = PropertyValues()
    test_property_values.address = 'Unit 56, 345 Fawkes Street, North Balk, NSW 3222'
    test_property_values.property_type = 'Landed Property'
    test_property_values.rent_type = 'Whole Property'
    test_property_values.description = 'Description 1'
    test_property_values.parking = False
    test_property_values.rent_cost = 456.22

    test_property_values_2 = PropertyValues()
    test_property_values_2.address = 'Unit 45, 345 Faes Drive, North Balk, NSW 3222'
    test_property_values_2.property_type = 'Apartment'
    test_property_values_2.rent_type = 'Private Room'
    test_property_values_2.description = 'Description 2'
    test_property_values_2.parking = True
    test_property_values_2.rent_cost = 650.09

    test_property_values_3 = PropertyValues()
    test_property_values_3.address = '345 Unit Street, North Balk, NSW 3222'
    test_property_values_3.property_type = 'Landed Property'
    test_property_values_3.rent_type = 'Private Room'
    test_property_values_3.description = 'Description 3'
    test_property_values_3.parking = True
    test_property_values_3.rent_cost = 1000.05

    test_property_values_4 = PropertyValues()
    test_property_values_4.address = '345 Test Street, North Balk, NSW 3222'
    test_property_values_4.property_type = 'Apartment'
    test_property_values_4.rent_type = 'Private Room'
    test_property_values_4.description = 'Description 4 3 2 1'
    test_property_values_4.parking = True
    test_property_values_4.rent_cost = 750

    test_property_values_5 = PropertyValues()
    test_property_values_5.address = '345 UAT Street, North Balk, NSW 3222'
    test_property_values_5.property_type = 'Landed Property'
    test_property_values_5.rent_type = 'Private Room'
    test_property_values_5.description = 'Description 5 Words Words Words'
    test_property_values_5.parking = False
    test_property_values_5.rent_cost = 200

    test_fake_token = ''.join(random.choices(
        string.ascii_letters + string.digits, k=16))

    def setup_actions(self):
        ''' Initialize Action objects '''
        self.user_register = RegisterUser(self)
        self.add_property = AddProperty(self)
        self.add_property_bad_token = AddPropertyBadToken(self)
        self.edit_property = EditProperty(self)
        self.edit_property_bad_token = EditPropertyBadToken(self)
        self.edit_nonexistent_property = EditNonexistentProperty(self)
        self.get_property = GetProperty(self)
        self.get_nonexistent_property = GetNonexistentProperty(self)
        self.get_property_bad_token = GetPropertyBadToken(self)
        self.list_property = ListProperty(self)
        self.list_property_no_property = ListPropertyNoProperty(self)
        self.delete_property = DeleteProperty(self)
        self.delete_nonexistent_property = DeleteNonexistentProperty(self)

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

    def test_get_property(self):
        ''' Test getting property data '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.get_property.run(data_user['auth_token'],
                                  data_property['data']['property'][0]['id'],
                                  self.test_property_values)

    def test_get_property_with_invalid_token(self):
        ''' Test getting property with invalid token '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.get_property_bad_token.run(
                self.test_fake_token,
                data_property['data']['property'][0]['id'],
                self.test_property_values
            )

    def test_get_nonexistent_property(self):
        ''' Test getting data for property that doesn't exists '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            self.add_property.run(data_user['auth_token'],
                                  self.test_property_values)
            self.get_nonexistent_property.run(data_user['auth_token'], 3,
                                              self.test_property_values_3)

    def test_get_property_not_belonging_to_user(self):
        ''' Test getting property that does not_belong to user '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_user_2 = self.user_register.run(self.test_user_values_2)
            self.add_property.run(data_user['auth_token'],
                                  self.test_property_values)
            data_property_2 = self.add_property.run(data_user_2['auth_token'],
                                                    self.test_property_values_2)
            self.get_nonexistent_property.run(
                data_user['auth_token'],
                data_property_2['data']['property'][0]['id'],
                self.test_property_values_2
            )

    def test_edit_property_first_time(self):
        '''
        Test editing property for the first time. This is slightly different
        from further edits as onbly some property fields are filled in after
        adding
        '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.edit_property.run(data_user['auth_token'],
                                   data_property['data']['property'][0]['id'],
                                   self.test_property_values)

    def test_edit_property(self):
        ''' Test editing property '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.edit_property.run(data_user['auth_token'],
                                   data_property['data']['property'][0]['id'],
                                   self.test_property_values)
            self.edit_property.run(data_user['auth_token'],
                                   data_property['data']['property'][0]['id'],
                                   self.test_property_values_2)

    def test_edit_nonexistent_property(self):
        ''' Test getting data for property that doesn't exists '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.edit_nonexistent_property.run(data_user['auth_token'], 2,
                                               self.test_property_values_2)
            # make sure first property wasn't changed
            self.get_property.run(data_user['auth_token'],
                                  data_property['data']['property'][0]['id'],
                                  self.test_property_values)

    def test_edit_property_with_invalid_token(self):
        ''' Test editing property with invalid token '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            self.edit_nonexistent_property.run(
                self.test_fake_token,
                data_property['data']['property'][0]['id'],
                self.test_property_values_2
            )

    def test_edit_property_not_belonging_to_user(self):
        ''' Test editing property that does not_belong to user '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_user_2 = self.user_register.run(self.test_user_values_2)
            self.add_property.run(data_user['auth_token'],
                                  self.test_property_values)
            data_property_2 = self.add_property.run(data_user_2['auth_token'],
                                                    self.test_property_values_2)
            self.edit_nonexistent_property.run(
                data_user['auth_token'],
                data_property_2['data']['property'][0]['id'],
                self.test_property_values_3
            )
            # Make sure porperty 2 isn't affected
            self.get_property.run(data_user_2['auth_token'],
                                  data_property_2['data']['property'][0]['id'],
                                  self.test_property_values_2)

    def test_delete_property(self):
        ''' Test deleting property '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_property = self.add_property.run(data_user['auth_token'],
                                                  self.test_property_values)
            data_property_2 = self.add_property.run(data_user['auth_token'],
                                                    self.test_property_values_2)
            self.delete_property.run(data_user['auth_token'],
                                     data_property['data']['property'][0]['id'])
            # Make sure porperty 2 isn't affected
            self.get_property.run(data_user['auth_token'],
                                  data_property_2['data']['property'][0]['id'],
                                  self.test_property_values_2)

    def test_delete_nonexistent_property(self):
        ''' Test nonexistent deleting property '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            self.add_property.run(data_user['auth_token'],
                                  self.test_property_values)
            data_property_2 = self.add_property.run(data_user['auth_token'],
                                                    self.test_property_values_2)
            self.delete_nonexistent_property.run(data_user['auth_token'], 4)
            # Make sure porperty 2 isn't affected
            self.get_property.run(data_user['auth_token'],
                                  data_property_2['data']['property'][0]['id'],
                                  self.test_property_values_2)

    def test_delete_property_not_belonging_to_user(self):
        ''' Test deleting property that does not_belong to user '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            data_user_2 = self.user_register.run(self.test_user_values_2)
            self.add_property.run(data_user['auth_token'],
                                  self.test_property_values)
            data_property_2 = self.add_property.run(data_user_2['auth_token'],
                                                    self.test_property_values_2)
            self.delete_nonexistent_property.run(
                data_user['auth_token'],
                data_property_2['data']['property'][0]['id']
            )
            # Make sure porperty 2 isn't affected
            self.get_property.run(data_user_2['auth_token'],
                                  data_property_2['data']['property'][0]['id'],
                                  self.test_property_values_2)

    def test_list_property_with_no_property(self):
        ''' Test list property with account that has no property '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            self.list_property_no_property.run(data_user['auth_token'], {})

    def test_list_property_after_add(self):
        ''' Test list property after adding properties '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            test_property_id_values_dict = {}
            for test_property_values in [self.test_property_values,
                                         self.test_property_values_2,
                                         self.test_property_values_5]:
                data_property = self.add_property.run(data_user['auth_token'],
                                                      test_property_values)
                test_property_id_values_dict[
                    data_property['data']['property'][0]['id']
                ] = test_property_values
            self.list_property.run(data_user['auth_token'],
                                   test_property_id_values_dict)

    def test_list_property_after_add_edit(self):
        ''' Test list property after adding and editing properties '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            test_property_id_values_dict = {}
            for test_property_values in [self.test_property_values,
                                         self.test_property_values_2,
                                         self.test_property_values_5]:
                data_property = self.add_property.run(data_user['auth_token'],
                                                      test_property_values)
                test_property_id_values_dict[
                    data_property['data']['property'][0]['id']
                ] = test_property_values
            # Edit two random test_property_values
            edit_id = random.choice(list(test_property_id_values_dict.keys()))
            self.edit_property.run(data_user['auth_token'], edit_id,
                                   self.test_property_values_4)
            test_property_id_values_dict[edit_id] = self.test_property_values_4
            edit_id = random.choice(list(test_property_id_values_dict.keys()))
            self.edit_property.run(data_user['auth_token'], edit_id,
                                   self.test_property_values_3)
            test_property_id_values_dict[edit_id] = self.test_property_values_3
            # Test propetry list correctness after editing
            self.list_property.run(data_user['auth_token'],
                                   test_property_id_values_dict)

    def test_list_property_after_add_edit_delete(self):
        ''' Test list property after adding, editing and deleting properties '''
        with self.client:
            data_user = self.user_register.run(self.test_user_values)
            test_property_id_values_dict = {}
            for test_property_values in [self.test_property_values,
                                         self.test_property_values_2,
                                         self.test_property_values_3,
                                         self.test_property_values_5]:
                data_property = self.add_property.run(data_user['auth_token'],
                                                      test_property_values)
                test_property_id_values_dict[
                    data_property['data']['property'][0]['id']
                ] = test_property_values
            # Edit a random test_property_values
            edit_id = random.choice(list(test_property_id_values_dict.keys()))
            self.edit_property.run(data_user['auth_token'], edit_id,
                                   self.test_property_values_4)
            test_property_id_values_dict[edit_id] = self.test_property_values_4
            # Delete one random test_property_values
            edit_id = random.choice(list(test_property_id_values_dict.keys()))
            self.delete_property.run(data_user['auth_token'], edit_id)
            test_property_id_values_dict[edit_id] = None
            # Test propetry list correctness after editing
            self.list_property.run(data_user['auth_token'],
                                   test_property_id_values_dict)


if __name__ == '__main__':
    unittest.main()
