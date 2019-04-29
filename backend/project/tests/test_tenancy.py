'''
Tenancy API endpoint test cases
'''

import unittest

from project.tests.base import BaseTestCase
from project.tests.actions.user import RegisterUser
from project.tests.actions.add_new_tenancy import (
    AddNewTenancyWithCashDetails,
    AddNewTenancyWithPaypalDetails,
    AddNewTenancyWithBankDetails,
    AddNewTenancyBadRequest,
    AddNewTenancyInvalidAuthentication
)
from project.tests import values

class TestAddTenancyAPI(BaseTestCase):
    ''' Test views in Property Blueprint '''
    def setup_actions(self):
        ''' Initialize Action objects '''
        self.register_user = RegisterUser(self)
        self.add_new_tenancy_with_cash = AddNewTenancyWithCashDetails(self)
        self.add_new_tenancy_with_paypal = AddNewTenancyWithPaypalDetails(self)
        self.add_new_tenancy_with_bank = AddNewTenancyWithBankDetails(self)
        self.add_new_tenancy_bad_request = AddNewTenancyBadRequest(self)
        self.add_new_tenancy_bad_auth = AddNewTenancyInvalidAuthentication(self)

    def test_add_tenancy_with_cash_details(self):
        ''' Test adding new tenancy with cash payment method '''
        with self.client:
            user_data = self.register_user.run(
                values.auth_values.test_user_values['user_1']
            )
            self.add_new_tenancy_with_cash.run(
                user_data['auth_token'],
                values.tenancy_values.test_new_tenancy_values['with_cash']
            )
    
    def test_add_tenancy_with_paypal_details(self):
        ''' Test adding new tenancy with paypal payment method '''
        with self.client:
            user_data = self.register_user.run(
                values.auth_values.test_user_values['user_1']
            )
            self.add_new_tenancy_with_paypal.run(
                user_data['auth_token'],
                values.tenancy_values.test_new_tenancy_values['with_paypal']
            )
    
    def test_add_tenancy_with_bank_details(self):
        ''' Test adding new tenancy with bank payment method '''
        with self.client:
            user_data = self.register_user.run(
                values.auth_values.test_user_values['user_1']
            )
            self.add_new_tenancy_with_bank.run(
                user_data['auth_token'],
                values.tenancy_values.test_new_tenancy_values[
                    'with_bank_transfer'
                ]
            )
    
    def test_add_tenancy_with_invalid_token(self):
        ''' Test adding new tenancy with invalid token '''
        with self.client:
            user_data = self.register_user.run(
                values.auth_values.test_user_values['user_1']
            )
            self.add_new_tenancy_bad_request.run(
                user_data['auth_token'],
                values.tenancy_values.test_new_tenancy_values[
                    'with_bad_types'
                ]
            )
    
    def test_add_tenancy_with_bad_foriegn_table_values(self):
        ''' Test adding new tenancy with bad foriegn table values '''
        with self.client:
            self.register_user.run(
                values.auth_values.test_user_values['user_1']
            )
            self.add_new_tenancy_bad_auth.run(
                'h9h(H(h980h9h3232',
                values.tenancy_values.test_new_tenancy_values['with_cash']
            )


if __name__ == '__main__':
    unittest.main()
