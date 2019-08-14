# '''
# Paymetn details model test cases
# '''

# import unittest

# from project.tests.base import BaseTestCase
# from project.tests.actions.user import RegisterUser, RegisterUserApiAction
# from project.tests.actions.update_payment_details import (
#     AddPaymentDetailsAction,
#     ChkCashDetailsAction,
#     ChkPayPalDetailsAction,
#     ChkBankDetailsAction,
#     ChkPaymentDetailsFetcherAllAction,
#     ChkPaymentDetailsFetcherNoneAction,
#     ChkPaymentDetailsFetcherWithoutCash,
#     ChkPaymentDetailsFetcherWithoutPaypal,
#     ChkPaymentDetailsFetcherWithoutBankTrans,
#     ChkPaymentDetailsFetcherCashOnly,
#     ChkPaymentDetailsFetcherPayPalOnly,
#     ChkPaymentDetailsFetcherBankTransOnly
# )
# from project.server import db
# from project.server.models.auth import User
# from project.server.models.payment_details import (CashDetails, PaypalDetails,
#                                                    BankDetails,
#                                                    PaymentDetailsUpdater,
#                                                    PaymentDetailsFetcher)
# from project.tests import values


# def register_user_get_account_id(test_cls):
#     RegisterUserApiAction.run(test_cls,
#                               values.auth_values.test_user_values[
#                                   'user_1'
#                               ])
#     return db.session.query(User.account_id).filter(
#         User.email == values.auth_values.test_user_values[
#             'user_1'
#         ].email
#     ).first()[0]


# class TestPaymentDetailsUpdater(BaseTestCase):
#     ''' Test Payment Details model and helpers '''
#     def setup_actions(self):
#         ''' Initialize Action objects '''
#         self.register_user = RegisterUser(self)
    
#     def test_add_cash_payment_details(self):
#         ''' '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details['Cash']
#             )
#             ChkCashDetailsAction.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details['Cash']
#             )
        
#     def test_add_paypal_payment_details(self):
#         ''' '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details['PayPal']
#             )
#             ChkPayPalDetailsAction.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details['PayPal']
#             )
    
#     def test_add_banktransfer_payment_details(self):
#         ''' '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ]
#             )
#             ChkBankDetailsAction.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ]
#             )

# class TestPaymentDetailsFetcher(BaseTestCase):
#     ''' Test Payment Details model and helpers '''
#     def setup_actions(self):
#         ''' Initialize Action objects '''
#         self.register_user = RegisterUser(self)

#     def test_fetch_payment_details_all_available(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ]
#             )
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ]
#             )
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ]
#             )
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherAllAction.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )


#     def test_fetch_payment_details_all_missing(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherNoneAction.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )

#     def test_fetch_payment_details_cash_missing(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ]
#             )
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ]
#             )
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherWithoutCash.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )

#     def test_fetch_payment_details_paypal_missing(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ]
#             )
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ]
#             )
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherWithoutPaypal.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )

#     def test_fetch_payment_details_banktransfer_missing(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ]
#             )
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ]
#             )
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherWithoutBankTrans.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )

#     def test_fetch_payment_details_cash_only(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Cash'
#                 ]
#             )
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherCashOnly.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )

#     def test_fetch_payment_details_paypal_only(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'PayPal'
#                 ]
#             )
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherPayPalOnly.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )

#     def test_fetch_payment_details_banktransfer_only(self):
#         '''  '''
#         with self.client:
#             account_id = register_user_get_account_id(self)
#             AddPaymentDetailsAction.run(
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ].payment_method,
#                 account_id,
#                 values.payment_details_values.test_payment_details[
#                     'Bank Transfer'
#                 ]
#             )
#             pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
#             ChkPaymentDetailsFetcherBankTransOnly.run(
#                 self,
#                 account_id,
#                 values.payment_details_values.test_payment_details,
#                 pd_fetcher.payment_details_to_dict()
#             )

# if __name__ == '__main__':
#     unittest.main()
