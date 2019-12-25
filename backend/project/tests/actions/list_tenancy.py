import json
from datetime import datetime

from project.server import db
from project.server import app
from project.tests.base import BaseTestCase
from project.server.models.type_values import (PaymentMethod, PaymentTerms,
                                               RentType)
from project.server.models.tenancy import Tenancy, TenancyHistory
from project.server.models.tenant import Tenant
from project.server.models.payment_details import (CashDetails, PaypalDetails,
                                                   BankDetails)


class ListTenancyApiAction():
    @staticmethod
    def run(test_cls, auth_token):
        ''' add tenancy via api '''
        return test_cls.client.get(
            '/tenancy/list',
            headers=dict(Authorization='Bearer ' + auth_token)
        )


class ChkListTenancyResponseAction():
    @staticmethod
    def run(test_cls, test_tenancy_list_dict, response):
        data = json.loads(response.data.decode())
        test_cls.assertEqual(data['status'], 'success')
        test_cls.assertEqual(response.content_type,
                             'application/json')
        test_cls.assertEqual(response.status_code, 200)
        test_cls.assertIn('d', data)
        test_cls.assertIn('tenancy_list', data['d'])
        response_tenancy_dict = dict()
        for tenancy_item in data['d']['tenancy_list']:
            response_tenancy_dict[tenancy_item['Tenancy']['id']] = tenancy_item
        test_cls.assertEqual(set(
            tid for tid in test_tenancy_list_dict
        ) ^ set(rid for rid in response_tenancy_dict), set())
        for _id in test_tenancy_list_dict:
            test_cls.assertIn(_id, response_tenancy_dict)
            test_cls.assertEqual(test_tenancy_list_dict[_id]['start_date'],
                                 response_tenancy_dict[_id]['Tenancy']['start_date'])
            test_cls.assertEqual(test_tenancy_list_dict[_id]['end_date'],
                                 response_tenancy_dict[_id]['Tenancy']['end_date'])
            test_cls.assertEqual(test_tenancy_list_dict[_id]['address'],
                                 response_tenancy_dict[_id]['Tenancy']['address'])
            test_cls.assertEqual(test_tenancy_list_dict[_id]['rent_type'],
                                 response_tenancy_dict[_id]['RentType'])
            test_cls.assertEqual(test_tenancy_list_dict[_id]['room_name'],
                                 response_tenancy_dict[_id]['Tenancy']['room_name'])
            test_cls.assertEqual(
                test_tenancy_list_dict[_id]['payment_terms'],
                response_tenancy_dict[_id]['PaymentTerms']
            )
            test_cls.assertEqual(test_tenancy_list_dict[_id]['rent_cost'],
                                 response_tenancy_dict[_id]['Tenancy']['rent_cost'])
            test_cls.assertIsNone(response_tenancy_dict[_id]['Tenancy']['notes'])
