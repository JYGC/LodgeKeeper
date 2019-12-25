from project.tests.base import BaseTestCase
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


class ChkPaymentDetailsAction():
    payment_detail_class = None

    @classmethod
    def run(self, test_cls, account_id, test_payment_details):
        db_payment_details = db.session.query(
            self.payment_detail_class
        ).filter(self.payment_detail_class.account_id == account_id).all()
        self._test_assertions(test_cls, account_id, test_payment_details,
                              db_payment_details)
    
    @staticmethod
    def _test_assertions(test_cls, account_id, test_payment_details,
                         db_payment_details):
        pass


class ChkCashDetailsAction(ChkPaymentDetailsAction):
    payment_detail_class = CashDetails
    
    @staticmethod
    def _test_assertions(test_cls, account_id, test_payment_details,
                         db_payment_details):
        test_cls.assertEqual(len(db_payment_details), 1)
        test_cls.assertEqual(db_payment_details[0].description,
                             test_payment_details.description)


class ChkPayPalDetailsAction(ChkPaymentDetailsAction):
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


class ChkBankDetailsAction(ChkPaymentDetailsAction):
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
                             

class ChkPaymentDetailsFetcher():
    @staticmethod
    def _test_cash_assertions(test_cls, test_cash_details,
                              cash_details_dict):
        pass

    @staticmethod
    def _test_paypal_assertions(test_cls, test_paypal_details,
                                paypal_details_dict):
        pass

    @staticmethod
    def _test_banktransfer_assertions(test_cls, test_banktransfer_details,
                                      banktransfer_details_dict):
        pass

    @classmethod
    def run(self, test_cls, account_id, test_payment_details,
            payment_details_dict):
        self._test_cash_assertions(test_cls, test_payment_details['Cash'],
                                   payment_details_dict['Cash'])
        self._test_paypal_assertions(test_cls, test_payment_details['PayPal'],
                                     payment_details_dict['PayPal'])
        self._test_banktransfer_assertions(
            test_cls,
            test_payment_details['Bank Transfer'],
            payment_details_dict['Bank Transfer']
        )


class ChkPaymentDetailsFetcherWithCashPart():
    @staticmethod
    def _test_cash_assertions(test_cls, test_cash_details,
                              cash_details_dict):
        test_cls.assertEqual(test_cash_details.description,
                             cash_details_dict['description'])


class ChkPaymentDetailsFetcherWithPayPalPart():
    @staticmethod
    def _test_paypal_assertions(test_cls, test_paypal_details,
                                paypal_details_dict):
        test_cls.assertEqual(test_paypal_details.description,
                             paypal_details_dict['description'])
        test_cls.assertEqual(test_paypal_details.email,
                             paypal_details_dict['email'])
        test_cls.assertEqual(test_paypal_details.reason,
                             paypal_details_dict['reason'])
        test_cls.assertEqual(test_paypal_details.message,
                             paypal_details_dict['message'])


class ChkPaymentDetailsFetcherWithBankTransPart():
    @staticmethod
    def _test_banktransfer_assertions(test_cls, test_banktransfer_details,
                                      banktransfer_details_dict):
        test_cls.assertEqual(test_banktransfer_details.description,
                             banktransfer_details_dict['description'])
        test_cls.assertEqual(test_banktransfer_details.bank_name,
                             banktransfer_details_dict['bank_name'])
        test_cls.assertEqual(test_banktransfer_details.account_name,
                             banktransfer_details_dict['account_name'])
        test_cls.assertEqual(test_banktransfer_details.bsb_number,
                             banktransfer_details_dict['bsb_number'])
        test_cls.assertEqual(test_banktransfer_details.account_number,
                             banktransfer_details_dict['account_number'])


class ChkPaymentDetailsFetcherWithoutCashPart():
    @staticmethod
    def _test_cash_assertions(test_cls, test_cash_details,
                              cash_details_dict):
        test_cls.assertIsNone(cash_details_dict)


class ChkPaymentDetailsFetcherWithoutPayPalPart():
    @staticmethod
    def _test_paypal_assertions(test_cls, test_paypal_details,
                                paypal_details_dict):
        test_cls.assertIsNone(paypal_details_dict)


class ChkPaymentDetailsFetcherWithoutBankTransPart():
    @staticmethod
    def _test_banktransfer_assertions(test_cls, test_banktransfer_details,
                                      banktransfer_details_dict):
        test_cls.assertIsNone(banktransfer_details_dict)


class ChkPaymentDetailsFetcherAllAction(
    ChkPaymentDetailsFetcherWithCashPart,
    ChkPaymentDetailsFetcherWithPayPalPart,
    ChkPaymentDetailsFetcherWithBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass


class ChkPaymentDetailsFetcherNoneAction(
    ChkPaymentDetailsFetcherWithoutCashPart,
    ChkPaymentDetailsFetcherWithoutPayPalPart,
    ChkPaymentDetailsFetcherWithoutBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass


class ChkPaymentDetailsFetcherWithoutCash(
    ChkPaymentDetailsFetcherWithoutCashPart,
    ChkPaymentDetailsFetcherWithPayPalPart,
    ChkPaymentDetailsFetcherWithBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass


class ChkPaymentDetailsFetcherWithoutPaypal(
    ChkPaymentDetailsFetcherWithCashPart,
    ChkPaymentDetailsFetcherWithoutPayPalPart,
    ChkPaymentDetailsFetcherWithBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass


class ChkPaymentDetailsFetcherWithoutBankTrans(
    ChkPaymentDetailsFetcherWithCashPart,
    ChkPaymentDetailsFetcherWithPayPalPart,
    ChkPaymentDetailsFetcherWithoutBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass


class ChkPaymentDetailsFetcherCashOnly(
    ChkPaymentDetailsFetcherWithCashPart,
    ChkPaymentDetailsFetcherWithoutPayPalPart,
    ChkPaymentDetailsFetcherWithoutBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass


class ChkPaymentDetailsFetcherPayPalOnly(
    ChkPaymentDetailsFetcherWithoutCashPart,
    ChkPaymentDetailsFetcherWithPayPalPart,
    ChkPaymentDetailsFetcherWithoutBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass


class ChkPaymentDetailsFetcherBankTransOnly(
    ChkPaymentDetailsFetcherWithoutCashPart,
    ChkPaymentDetailsFetcherWithoutPayPalPart,
    ChkPaymentDetailsFetcherWithBankTransPart,
    ChkPaymentDetailsFetcher
):
    pass
