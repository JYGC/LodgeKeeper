'''
Paymetn details model test cases
'''

import unittest

from project.tests.base import BaseTestCase
from project.tests.actions.user import RegisterUser, RegisterUserApiAction
from project.tests.actions.update_payment_details import (
    AddPaymentDetailsAction,
    CheckCashDetailsAction,
    CheckPayPalDetailsAction,
    CheckBankDetailsAction
)
from project.server import db
from project.server.models.auth import User
from project.server.models.payment_details import (CashDetails, PaypalDetails,
                                                   BankDetails,
                                                   PaymentDetailsUpdater,
                                                   PaymentDetailsFetcher)
from project.tests import values


def register_user_get_account_id(test_cls):
    RegisterUserApiAction.run(test_cls,
                              values.auth_values.test_user_values[
                                  'user_1'
                              ])
    return db.session.query(User.account_id).filter(
        User.email == values.auth_values.test_user_values[
            'user_1'
        ].email
    ).first()[0]


class TestPaymentDetailsUpdater(BaseTestCase):
    ''' Test Payment Details model and helpers '''
    def setup_actions(self):
        ''' Initialize Action objects '''
        self.register_user = RegisterUser(self)
    
    def test_add_cash_payment_details(self):
        ''' '''
        with self.client:
            account_id = register_user_get_account_id(self)
            AddPaymentDetailsAction.run(
                values.payment_details_values.test_payment_details[
                    'cash'
                ].payment_method,
                account_id,
                values.payment_details_values.test_payment_details['cash']
            )
            CheckCashDetailsAction.run(
                self,
                account_id,
                values.payment_details_values.test_payment_details['cash']
            )
        
    def test_add_paypal_payment_details(self):
        ''' '''
        with self.client:
            account_id = register_user_get_account_id(self)
            AddPaymentDetailsAction.run(
                values.payment_details_values.test_payment_details[
                    'paypal'
                ].payment_method,
                account_id,
                values.payment_details_values.test_payment_details['paypal']
            )
            CheckPayPalDetailsAction.run(
                self,
                account_id,
                values.payment_details_values.test_payment_details['paypal']
            )
    
    def test_add_banktransfer_payment_details(self):
        ''' '''
        with self.client:
            account_id = register_user_get_account_id(self)
            AddPaymentDetailsAction.run(
                values.payment_details_values.test_payment_details[
                    'banktransfer'
                ].payment_method,
                account_id,
                values.payment_details_values.test_payment_details[
                    'banktransfer'
                ]
            )
            CheckBankDetailsAction.run(
                self,
                account_id,
                values.payment_details_values.test_payment_details[
                    'banktransfer'
                ]
            )

class TestPaymentDetailsFetcher(BaseTestCase):
    ''' Test Payment Details model and helpers '''
    def setup_actions(self):
        ''' Initialize Action objects '''
        self.register_user = RegisterUser(self)

    def test_fetch_payment_details_all_available(self):
        '''  '''
        with self.client:
            account_id = register_user_get_account_id(self)
            AddPaymentDetailsAction.run(
                values.payment_details_values.test_payment_details[
                    'cash'
                ].payment_method,
                account_id,
                values.payment_details_values.test_payment_details[
                    'cash'
                ]
            )
            AddPaymentDetailsAction.run(
                values.payment_details_values.test_payment_details[
                    'paypal'
                ].payment_method,
                account_id,
                values.payment_details_values.test_payment_details[
                    'paypal'
                ]
            )
            AddPaymentDetailsAction.run(
                values.payment_details_values.test_payment_details[
                    'banktransfer'
                ].payment_method,
                account_id,
                values.payment_details_values.test_payment_details[
                    'banktransfer'
                ]
            )

            pd_fetcher = PaymentDetailsFetcher(db.session, account_id)


    def test_fetch_payment_details_all_missing(self):
        '''  '''
        with self.client:
            account_id = register_user_get_account_id(self)
            pd_fetcher = PaymentDetailsFetcher(db.session, account_id)

    def test_fetch_payment_details_cash_missing(self):
        '''  '''
        with self.client:
            self.assertTrue(False)

    def test_fetch_payment_details_paypal_missing(self):
        '''  '''
        with self.client:
            self.assertTrue(False)

    def test_fetch_payment_details_banktransfer_missing(self):
        '''  '''
        with self.client:
            self.assertTrue(False)

    def test_fetch_payment_details_cash_only(self):
        '''  '''
        with self.client:
            self.assertTrue(False)

    def test_fetch_payment_details_paypal_only(self):
        '''  '''
        with self.client:
            self.assertTrue(False)

    def test_fetch_payment_details_banktransfer_only(self):
        '''  '''
        with self.client:
            self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
