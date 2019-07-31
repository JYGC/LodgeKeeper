from project.tests.base import BaseTestCase
from project.tests.actions.abcs import (IAction, IApiCheckAction,
                                        IDbCheckAction)
from project.server import db
from project.server.models.payment_details import (CashDetails, PaypalDetails,
                                                   BankDetails,
                                                   PaymentDetailsUpdater,
                                                   PaymentDetailsFetcher)


class AddPaymentDetailsAction():
    @staticmethod
    def run(payment_method, account_id, test_payment_details):
        cash_updater = PaymentDetailsUpdater(db.session, payment_method,
                                             account_id)
        db.session.add(cash_updater.dict_to_payment_details(
            test_payment_details.__dict__
        ))


class CheckPaymentDetailsAction():
    payment_detail_class = None

    @classmethod
    def run(self, test_cls, account_id, test_payment_details):
        db_payment_details = db.session.query(
            self.payment_detail_class
        ).filter(self.payment_detail_class.account_id == account_id).all()
        self._test_assertions(test_cls, account_id, test_payment_details,
                              db_payment_details)
    
    @staticmethod
    def _test_assertions(test_cls, account_id, test_payment_details, db_payment_details):
        pass


class CheckCashDetailsAction(CheckPaymentDetailsAction):
    payment_detail_class = CashDetails
    
    @staticmethod
    def _test_assertions(test_cls, account_id, test_payment_details,
                         db_payment_details):
        test_cls.assertEqual(len(db_payment_details), 1)
        test_cls.assertEqual(db_payment_details[0].description,
                             test_payment_details.description)


class CheckPayPalDetailsAction(CheckPaymentDetailsAction):
    payment_detail_class = PaypalDetails
    
    @staticmethod
    def _test_assertions(test_cls, account_id, test_payment_details,
                         db_payment_details):
        test_cls.assertEqual(len(db_payment_details), 1)
        test_cls.assertEqual(db_payment_details[0].description,
                             test_payment_details.description)
        test_cls.assertEqual(db_payment_details[0].email,
                             test_payment_details.email)
        test_cls.assertEqual(db_payment_details[0].reason,
                             test_payment_details.reason)
        test_cls.assertEqual(db_payment_details[0].message,
                             test_payment_details.message)


class CheckBankDetailsAction(CheckPaymentDetailsAction):
    payment_detail_class = BankDetails
    
    @staticmethod
    def _test_assertions(test_cls, account_id, test_payment_details,
                         db_payment_details):
        test_cls.assertEqual(len(db_payment_details), 1)
        test_cls.assertEqual(db_payment_details[0].description,
                             test_payment_details.description
        )
        test_cls.assertEqual(db_payment_details[0].bank_name,
                             test_payment_details.bank_name)
        test_cls.assertEqual(db_payment_details[0].account_name,
                             test_payment_details.account_name)
        test_cls.assertEqual(db_payment_details[0].bsb_number,
                             test_payment_details.bsb_number)
        test_cls.assertEqual(db_payment_details[0].account_number,
                             test_payment_details.account_number)


class CheckPaymentDetailsFetcherAllAction():
    @classmethod
    def run(self, test_cls, account_id, test_payment_details,
            db_payment_details_dict):
        pd_fetcher = PaymentDetailsFetcher(db.session, account_id)
        payment_details_dict = pd_fetcher.payment_details_to_dict()

        self._test_cash_assertions(test_cls, test_payment_details['cash'],
                                   payment_details_dict['Cash'])
        self._test_paypal_assertions(test_cls, test_payment_details['paypal'],
                                     payment_details_dict['PayPal'])
        self._test_banktransfer_assertions(
            test_cls,
            test_payment_details['banktransfer'],
            payment_details_dict['Bank Transfer']
        )
    
    @staticmethod
    def _test_cash_assertions(test_cls, test_cash_details,
                              cash_details_dict):
        test_cls.assertIn(test_cash_details.payment_method,
                          cash_details_dict)
        #test_cls.assertEqual()
    
    @staticmethod
    def _test_paypal_assertions(test_cls, test_paypal_details,
                                paypal_details_dict):
        test_cls.assertIn(test_paypal_details.payment_method,
                          paypal_details_dict)
    
    @staticmethod
    def _test_banktransfer_assertions(test_cls, test_banktransfer_details,
                                      banktransfer_details_dict):
        test_cls.assertIn(test_banktransfer_details.payment_method,
                          banktransfer_details_dict)
