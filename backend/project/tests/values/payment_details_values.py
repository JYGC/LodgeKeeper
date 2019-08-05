class IPaymentDetails():
    def __init__(self, description):
        self.description = description


class CashDetails(IPaymentDetails):
    def __init__(self, description=None):
        super().__init__(description)
        self.payment_method = 'Cash'


class PayPalDetails(IPaymentDetails):
    def __init__(self, description=None, paypal_email=None, reason=None,
                 message=None):
        super().__init__(description)
        self.payment_method = 'PayPal'
        self.email = paypal_email
        self.reason = reason
        self.message = message


class BankDetails(IPaymentDetails):
    def __init__(self, description=None, bank_name=None, account_name=None,
                 bsb_number=None, account_number=None):
        super().__init__(description)
        self.payment_method = 'Bank Transfer'
        self.bank_name = bank_name
        self.account_name = account_name
        self.bsb_number = bsb_number
        self.account_number = account_number

test_payment_details = {
    'Cash': CashDetails('Paid every week'),
    'PayPal': PayPalDetails('Tenant suggested using payment',
                            'jttff1@gmail.com', 'Rent payment', 'Rent payment'),
    'Bank Transfer': BankDetails('Payment every month, Bank details provided',
                                'Commonwealth Bank', 'Junying Chen', '356-398',
                                '739837409832740')
}
