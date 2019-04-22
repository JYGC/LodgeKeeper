import json

from project.server import db
from project.tests.base import BaseTestCase
from project.tests.actions.abcs import (IAction, IApiCheckAction,
                                        IDbCheckAction)
from project.tests.values.property_values import PropertyValues
from project.server.models.property import Property
from project.server.models.type_values import PropertyType, RentType

class AddProperty(IAction, IApiCheckAction, IDbCheckAction):
    ''' Add new property '''
    def __init__(self, test_cls: BaseTestCase):
        super().__init__(test_cls)

    def api_request(self, auth_token, test_values: PropertyValues):
        ''' add property via api '''
        return self.test_cls.client.post(
            '/property/add',
            headers=dict(Authorization='Bearer ' + auth_token),
            data=json.dumps(dict(
                address=test_values.address,
                property_type=test_values.property_type,
                rent_type=test_values.rent_type,
                description=test_values.description,
                parking=test_values.parking,
                rent_cost=test_values.rent_cost,
                date_constructed=test_values.date_constructed
            )),
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
        self.test_cls.assertIn('data', data)
        self.test_cls.assertIn('property', data['data'])
        self.test_cls.assertTrue(data['data']['property'][0]['id'])
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 201)

    def check_db_state(self, test_values: PropertyValues, data):
        property_list = db.session.query(
            Property,
            PropertyType,
            RentType
        ).outerjoin(
            PropertyType,
            Property.property_type_id == PropertyType.id
        ).outerjoin(
            RentType,
            Property.rent_type_id == RentType.id
        ).filter(Property.id == data['data']['property'][0]['id']).all()
        
        self.test_cls.assertEqual(len(property_list), 1)
        self.test_cls.assertEqual(property_list[0].Property.address,
                                  test_values.address)
        self.test_cls.assertEqual(property_list[0].PropertyType.value,
                                  test_values.property_type)
        self.test_cls.assertEqual(property_list[0].RentType.value,
                                  test_values.rent_type)
        self.test_cls.assertEqual(property_list[0].Property.description,
                                  test_values.description)
        self.test_cls.assertEqual(property_list[0].Property.parking,
                                  test_values.parking)
        self.test_cls.assertEqual(
            round(float(property_list[0].Property.rent_cost),2),
            test_values.rent_cost
        )
        self.test_cls.assertFalse(property_list[0].Property.is_deleted)

class AddPropertyBadToken(AddProperty):
    ''' Try adding new property with invalid token '''
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertNotIn('data', data)
        self.test_cls.assertEqual(data['message'],
                                  'Invalid token. Please log in again.')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 401)

    def check_db_state(self, test_values: PropertyValues, data):
        pass


class AddPropertyBadItemType(AddProperty):
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 400)

    def check_db_state(self, test_values: PropertyValues, data):
        pass


class GetProperty(IAction, IApiCheckAction):
    ''' Get property '''
    def __init__(self, test_cls: BaseTestCase):
        super().__init__(test_cls)

    def api_request(self, auth_token, property_id):
        ''' get property via api '''
        return self.test_cls.client.post(
            '/property/get',
            headers=dict(Authorization='Bearer ' + auth_token),
            data=json.dumps(dict(id=property_id)),
            content_type='application/json',
        )

    def run(self, auth_token, property_id, test_values: PropertyValues):
        resp_property = self.api_request(auth_token, property_id)
        data_property = json.loads(resp_property.data.decode())
        self.check_response(test_values, data_property, resp_property)
        return data_property

    def check_response(self, test_values: PropertyValues, data, resp):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertIn('data', data)
        self.test_cls.assertIn('property', data['data'])
        self.test_cls.assertEqual(len(data['data']['property']), 1)
        property_data = data['data']['property'][0]
        self.test_cls.assertEqual(property_data['address'], test_values.address)
        self.test_cls.assertEqual(property_data['property_type'],
                                  test_values.property_type)
        self.test_cls.assertEqual(property_data['rent_type'],
                                  test_values.rent_type)
        self.test_cls.assertEqual(property_data['description'],
                                  test_values.description)
        self.test_cls.assertEqual(bool(property_data['parking']),
                                  test_values.parking)
        self.test_cls.assertEqual(property_data['rent_cost'],
                                  test_values.rent_cost)
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 200)


class GetPropertyBadToken(GetProperty):
    ''' Try to get property with invalid token '''
    def check_response(self, test_values: PropertyValues, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertNotIn('data', data)
        self.test_cls.assertEqual(data['message'],
                                  'Invalid token. Please log in again.')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 401)


class GetNonexistentProperty(GetProperty):
    '''
    Delete nonexistent property or property that doesn't belong to the user via
    api
    '''
    def check_response(self, test_values: PropertyValues, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 400)


class EditProperty(IAction, IApiCheckAction, IDbCheckAction):
    ''' edit property '''
    def __init__(self, test_cls: BaseTestCase):
        super().__init__(test_cls)

    def api_request(self, auth_token, property_id,
                    test_values: PropertyValues):
        ''' edit property via api '''
        return self.test_cls.client.post(
            '/property/edit',
            headers=dict(Authorization='Bearer ' + auth_token),
            data=json.dumps(dict(
                id=property_id,
                address=test_values.address,
                property_type=test_values.property_type,
                rent_type=test_values.rent_type,
                description=test_values.description,
                parking=test_values.parking,
                rent_cost=test_values.rent_cost,
                date_constructed=test_values.date_constructed
            )),
            content_type='application/json',
        )

    def run(self, auth_token, property_id, test_values: PropertyValues):
        resp_property = self.api_request(auth_token, property_id, test_values)
        data_property = json.loads(resp_property.data.decode())
        self.check_response(data_property, resp_property)
        self.check_db_state(property_id, test_values)
        return data_property

    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 200)

    def check_db_state(self, property_id, test_values: PropertyValues):
        property_list = db.session.query(
            Property,
            PropertyType,
            RentType
        ).outerjoin(
            PropertyType,
            Property.property_type_id == PropertyType.id
        ).outerjoin(
            RentType,
            Property.rent_type_id == RentType.id
        ).filter(Property.id == property_id).all()

        self.test_cls.assertEqual(len(list(property_list)), 1)
        self.test_cls.assertEqual(property_list[0].Property.address,
                                  test_values.address)
        self.test_cls.assertEqual(property_list[0].PropertyType.value,
                                  test_values.property_type)
        self.test_cls.assertEqual(property_list[0].RentType.value,
                                  test_values.rent_type)
        self.test_cls.assertEqual(property_list[0].Property.description,
                                  test_values.description)
        self.test_cls.assertEqual(property_list[0].Property.parking,
                                  test_values.parking)
        self.test_cls.assertEqual(
            round(float(property_list[0].Property.rent_cost),2),
            test_values.rent_cost
        )
        self.test_cls.assertFalse(property_list[0].Property.is_deleted)


class EditPropertyBadToken(EditProperty):
    ''' edit property with invalid token '''
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertEqual(data['message'],
                                  'Invalid token. Please log in again.')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 401)

    def check_db_state(self, property_id, test_values: PropertyValues):
        pass


class EditNonexistentProperty(EditProperty):
    '''
    Edit nonexistent property or property that is not belonging to the user via
    api
    '''
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 400)

    def check_db_state(self, property_id, test_values: PropertyValues):
        pass


class EditPropertyBadItemType(EditNonexistentProperty):
    pass


class DeleteProperty(IAction, IApiCheckAction, IDbCheckAction):
    ''' Delete property '''
    def __init__(self, test_cls: BaseTestCase):
        super().__init__(test_cls)

    def api_request(self, auth_token, property_id):
        ''' Delete property via api '''
        return self.test_cls.client.post(
            '/property/delete',
            headers=dict(Authorization='Bearer ' + auth_token),
            data=json.dumps(dict(id=property_id)),
            content_type='application/json',
        )

    def run(self, auth_token, property_id):
        resp_property = self.api_request(auth_token, property_id)
        data_property = json.loads(resp_property.data.decode())
        self.check_response(data_property, resp_property)
        self.check_db_state(property_id)
        return data_property

    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 200)

    def check_db_state(self, property_id):
        property_list = db.session.query(Property).filter(
            Property.id == property_id
        )
        self.test_cls.assertEqual(len(list(property_list)), 1)
        self.test_cls.assertTrue(property_list[0].is_deleted)


class DeleteNonexistentProperty(DeleteProperty):
    '''
    Delete nonexistent property or delete porperty that doesn't belong to user
    via api
    '''
    def check_response(self, data, resp):
        self.test_cls.assertEqual(data['status'], 'fail')
        self.test_cls.assertEqual(resp.content_type, 'application/json')
        self.test_cls.assertEqual(resp.status_code, 400)

    def check_db_state(self, property_id):
        pass


class ListProperty(IAction, IApiCheckAction):
    ''' Get list of property belonging to user '''
    def __init__(self, test_cls: BaseTestCase):
        super().__init__(test_cls)

    def api_request(self, auth_token):
        ''' Get list of properties owned by user via api '''
        return self.test_cls.client.get(
            '/property',
            headers=dict(Authorization='Bearer ' + auth_token),
            content_type='application/json',
        )

    def run(self, auth_token, property_id_values_dict: dict):
        '''
        Run action. property_id_values_dict needs to be of the follwoing form:
        {..., property_id <int>: property_value <PropertyValue>, ...}.
        '''
        resp_property = self.api_request(auth_token)
        data_property = json.loads(resp_property.data.decode())
        self.check_response(property_id_values_dict, data_property,
                            resp_property)
        return data_property

    def check_response(self, property_id_values_dict: dict, data, resp):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertIn('data', data)
        self.test_cls.assertIn('property', data['data'])
        data_property_list = data['data']['property']
        data_property_dict = dict(zip(
            [cur_property['id'] for cur_property in data_property_list],
            data_property_list
        ))
        for property_id, property_value in property_id_values_dict.items():
            if (property_value == None):
                # if property_value is None we check to make sure it isn't in
                # the response becuase it is deleted
                self.test_cls.assertNotIn(property_id, data_property_dict)
            else:
                self.test_cls.assertIn(property_id, data_property_dict)
                self.test_cls.assertEqual(
                    data_property_dict[property_id]['address'],
                    property_value.address
                )
                self.test_cls.assertEqual(
                    data_property_dict[property_id]['property_type'], #
                    property_value.property_type
                )
                self.test_cls.assertEqual(
                    data_property_dict[property_id]['rent_type'],
                    property_value.rent_type
                )
                self.test_cls.assertEqual(
                    data_property_dict[property_id]['description'],
                    property_value.description
                )
                self.test_cls.assertEqual(
                    data_property_dict[property_id]['parking'],
                    property_value.parking
                )
                self.test_cls.assertEqual(
                    data_property_dict[property_id]['rent_cost'],
                    property_value.rent_cost
                )


class ListPropertyNoProperty(ListProperty):
    '''
    Get list of property belonging to user when user has not property listed
    '''
    def check_response(self, property_id_values_dict: dict, data, resp):
        self.test_cls.assertEqual(data['status'], 'success')
        self.test_cls.assertIn('data', data)
        self.test_cls.assertIn('property', data['data'])
        self.test_cls.assertEqual(len(data['data']['property']), 0)
