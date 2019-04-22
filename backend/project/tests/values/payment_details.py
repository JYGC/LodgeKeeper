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
        self.paypal_email = paypal_email
        self.reason = reason
        self.message = message


class BankTransfer(IPaymentDetails):
    def __init__(self, description=None, bank_name=None, account_name=None,
                 bsb_number=None, account_number=None):
        super().__init__(description)
        self.payment_method = 'Bank Transfer'
        self.bank_name = bank_name
        self.account_name = account_name
        self.bsb_number = bsb_number
        self.account_number = account_number
        