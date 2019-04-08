import json
from typing import Union

from project.server import db
from project.tests.base import BaseTestCase
from project.tests.values.property_values import PropertyValues
from project.server.models.property import Property, PropertyType, RentType

class AddProperty():
    ''' Add new property '''
    test_cls = None

    def __init__(self, test_cls: BaseTestCase):
        self.test_cls = test_cls
    
    def api_request(self, auth_token, test_values: PropertyValues):
        ''' add property via api '''
        return self.test_cls.client.post(
            '/property/add',
            headers=dict(
                Authorization='Bearer ' + auth_token
            ),
            data=json.dumps(dict(address=test_values.property_address,
                                property_type=test_values.property_type)),
            content_type='application/json',
        )

    def run(self, auth_token, test_values: PropertyValues):
        ''' run action '''
        resp_property = self.api_request(auth_token, test_values)
        data_property = json.loads(resp_property.data.decode())
        self.check_response(data_property, resp_property)
        self.check_db_state(test_values, data_property)
        return data_property

    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertTrue(data['property_id'])
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 201)

    def check_db_state(self, test_values: PropertyValues, data):
        property_list = db.session.query(Property.address).outerjoin(
            PropertyType,
            Property.property_type_id == PropertyType.id
        ).filter(Property.id == int(data['property_id']))
        self.test_cls.assertEqual(len(property_list), 1)
        self.test_cls.assertEqual(property_list[0].Property.address,
                            test_values.property_address)
        self.test_cls.assertEqual(property_list[0].PropertyType.value,
                            test_values.property_type)
        self.test_cls.assertFalse(property_list[0].Property.is_deleted)

class AddPropertyBadToken(AddProperty):
    ''' Try adding new property with invalid token '''
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertNotIn('property_id', data)
        self.test_cls.assertEqual(data['message'],
                            'Invalid token. Please log in again.')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 401)
    
    def check_db_state(self, test_values: PropertyValues, data):
        pass


class EditProperty():
    ''' edit property '''
    test_cls = None

    def __init__(self, test_cls: BaseTestCase):
        self.test_cls = test_cls
    
    def api_request(self, auth_token, property_id,
                    test_values: PropertyValues):
        ''' edit property via api '''
        return self.test_cls.client.post(
            '/property/edit',
            headers=dict(
                Authorization='Bearer ' + auth_token
            ),
            data=json.dumps(dict(id=property_id,
                                address=test_values.test_new_property_address,
                                property_type=test_values.test_new_property_type,
                                rent_type=test_values.test_new_rent_type,
                                description=test_values.test_new_description,
                                parking=test_values.test_new_parking,
                                rent_cost=test_values.test_new_rent_cost)),
            content_type='application/json',
        )

    def run(self, auth_token, property_id, test_values: PropertyValues):
        resp_property = self.api_request(auth_token, property_id, test_values)
        data_property = json.loads(resp_property.data.decode())
        self.check_response(data_property, resp_property)
        self.check_db_state(property_id, test_values, data_property)
        return data_property
    
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 200)

    def check_db_state(self, property_id, test_values, data):
        property_list = db.session.query(Property).outerjoin(
            PropertyType,
            Property.property_type_id == PropertyType.id
        ).outerjoin(
            RentType,
            Property.rent_type_id == RentType.id
        ).filter(Property.id == int(data['property_id']))
        self.check_db_state_assertions(test_values, property_list)

    def check_db_state_assertions(self, test_values: PropertyValues,
                                  property_list):
        self.test_cls.assertEqual(len(property_list), 1)
        self.test_cls.assertEqual(property_list[0].Property.address,
                                  property_list.property_address)
        self.test_cls.assertEqual(property_list[0].PropertyType.value,
                                  property_list.property_type)
        self.test_cls.assertEqual(property_list[0].Property.description,
                                  property_list.description)
        self.test_cls.assertEqual(property_list[0].Property.parking,
                                  property_list.parking)
        self.test_cls.assertEqual(property_list[0].Property.rent_cost,
                                  property_list.rent_cost)
        self.test_cls.assertFalse(property_list[0].Property.is_deleted)

class EditPropertyBadToken(EditProperty):
    ''' edit property with invalid token '''
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertEqual(data['message'],
                                  'Invalid token. Please log in again.')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 401)
    
    def check_db_state(self, property_id, test_values: PropertyValues, data):
        pass
