'''
Tenancy API endpoint test cases
'''

import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.actions.user import RegisterUser, RegisterUserApiAction
from project.tests.actions.list_tenancy import (
    ListTenancyApiAction,
    ChkListTenancyResponseAction
)
from project.tests.actions.add_new_tenancy import (
    AddTenancyApiAction,
    ChkAddTenancyResponseAction,
    ChkAddTenancyDbStateAction
)
from project.tests.actions.failed_response import (
    ChkResponseActionBadRequest,
    ChkResponseActionInvaildToken
)
from project.tests import values


def register_user_get_auth_token(test_cls):
    return json.loads(RegisterUserApiAction.run(
        test_cls,
        values.auth_values.test_user_values['user_1']
    ).data.decode())['auth_token']


class TestListTenancies(BaseTestCase):
    ''' Test list Tenancy endpoint '''

    def test_list_no_tenancies(self):
        ''' Test listing tenancies with no tenancies '''
        with self.client:
            ChkListTenancyResponseAction.run(
                self,
                dict(),
                ListTenancyApiAction.run(
                    self,
                    register_user_get_auth_token(self)
                )
            )

    def test_list_one_tenancy(self):
        ''' Test listing tenancies with one tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            tenancy_id = json.loads(AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['tenancy_list'][
                    2
                ],
                auth_token
            ).data.decode())['d']['tenancy_id']
            ChkListTenancyResponseAction.run(self, {
                tenancy_id: values.tenancy_values.test_new_tenancy_values[
                    'tenancy_list'
                ][2]
            }, ListTenancyApiAction.run(self, auth_token))

    def test_list_ten_tenancies(self):
        ''' Test listing tenancies with ten tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            test_tenancy_list_dict = dict()
            for test_tenancy in values.tenancy_values.test_new_tenancy_values[
                'tenancy_list'
            ]:
                test_tenancy_list_dict[
                    json.loads(AddTenancyApiAction.run(
                        self,
                        test_tenancy,
                        auth_token
                    ).data.decode())['d']['tenancy_id']
                ] = test_tenancy

            ChkListTenancyResponseAction.run(self, test_tenancy_list_dict,
                                             ListTenancyApiAction.run(
                                                 self,
                                                 auth_token
                                             ))


class TestAddTenancyAPI(BaseTestCase):
    ''' Test add tenancy endpoint '''
    
    def test_add_private_room_tenancy(self):
        ''' Test adding a new private room tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['private_room'],
                auth_token
            )
            ChkAddTenancyResponseAction.run(self, resp_addtenancy)
            ChkAddTenancyDbStateAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['private_room'],
                resp_addtenancy
            )
    
    def test_add_whole_property_tenancy(self):
        ''' Tets adding a new whole property tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['whole_property'],
                auth_token
            )
            ChkAddTenancyResponseAction.run(self, resp_addtenancy)
            ChkAddTenancyDbStateAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['whole_property'],
                resp_addtenancy
            )
    
    def test_add_tenancy_with_invalid_token(self):
        ''' Test adding new tenancy with invalid token '''
        with self.client:
            register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['private_room'],
                '000000000000000000000000'
            )
            ChkResponseActionInvaildToken.run(self, resp_addtenancy)
    
    def test_add_tenancy_with_bad_foriegn_table_values(self):
        ''' Test adding new tenancy with bad foriegn table values '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['with_bad_types'],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)
    
    def test_add_tenancy_no_tenants(self):
        ''' Test adding tenancy without tenants '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['no_tenants'],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)

    def test_add_tenancy_no_notifications(self):
        ''' Test adding tenancy without notifications '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values[
                    'no_notifications'
                ],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)

    def test_add_tenancy_no_tenants_and_notifications(self):
        ''' Test adding tenancy without tenants and notifications '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values[
                    'no_tenants_and_notifications'
                ],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)

    # def test_add_tenancy_with_cash_details(self):
    #     ''' Test adding new tenancy with cash payment method '''
    #     with self.client:
    #         user_data = self.register_user.run(
    #             values.auth_values.test_user_values['user_1']
    #         )
    #         self.add_new_tenancy_with_cash.run(
    #             user_data['auth_token'],
    #             values.tenancy_values.test_new_tenancy_values['with_cash']
    #         )
    
    # def test_add_tenancy_with_paypal_details(self):
    #     ''' Test adding new tenancy with paypal payment method '''
    #     with self.client:
    #         user_data = self.register_user.run(
    #             values.auth_values.test_user_values['user_1']
    #         )
    #         self.add_new_tenancy_with_paypal.run(
    #             user_data['auth_token'],
    #             values.tenancy_values.test_new_tenancy_values['with_paypal']
    #         )
    
    # def test_add_tenancy_with_bank_details(self):
    #     ''' Test adding new tenancy with bank payment method '''
    #     with self.client:
    #         user_data = self.register_user.run(
    #             values.auth_values.test_user_values['user_1']
    #         )
    #         self.add_new_tenancy_with_bank.run(
    #             user_data['auth_token'],
    #             values.tenancy_values.test_new_tenancy_values[
    #                 'with_bank_transfer'
    #             ]
    #         )


if __name__ == '__main__':
    unittest.main()
