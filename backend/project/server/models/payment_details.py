'''
Payment Details models and helper classes
'''

from sqlalchemy.ext.declarative import declared_attr

from project.server import db
from project.server.models.type_values import PaymentMethod


class IPaymentDetails():
    ''' Payment detils abstraction '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text)
    @declared_attr
    def account_id(self):
        return db.Column(db.Integer, db.ForeignKey('account.id'),
                         nullable=False)
    
    def dict_to_values(self, payment_details_dict):
        pass


class CashDetails(db.Model, IPaymentDetails):
    ''' Model for Cash payment details '''
    __tablename__ = 'cash_details'

    def dict_to_values(self, payment_details_dict):
        self.description = payment_details_dict['description']


class PaypalDetails(db.Model, IPaymentDetails):
    ''' Model for paypal details '''
    __tablename__ = 'paypal_details'
    email = db.Column(db.String(255))
    reason = db.Column(db.String(1024))
    message = db.Column(db.String(1024))

    def dict_to_values(self, payment_details_dict):
        self.description = payment_details_dict['description']
        self.email = payment_details_dict['email']
        self.reason = payment_details_dict['reason']
        self.message = payment_details_dict['message']


class BankDetails(db.Model, IPaymentDetails):
    ''' Model for bank details '''
    __tablename__ = 'bank_details'
    bank_name = db.Column(db.String(255))
    account_name = db.Column(db.String(255))
    bsb_number = db.Column(db.String(7))
    account_number = db.Column(db.String(255))

    def dict_to_values(self, payment_details_dict):
        self.description = payment_details_dict['description']
        self.bank_name = payment_details_dict['bank_name']
        self.account_name = payment_details_dict['account_name']
        self.bsb_number = payment_details_dict['bsb_number']
        self.account_number = payment_details_dict['account_number']


class PaymentDetailsPresenter():
    def __init__(self, db_session, payment_method, account_id):
        # Select PaymentDetails class
        if payment_method == 'Bank Transfer':
            payment_details_class = BankDetails
        elif payment_method == 'PayPal':
            payment_details_class = PaypalDetails
        elif payment_method == 'Cash':
            payment_details_class = CashDetails
        else:
            raise Exception('Unknown payment method')

        # Get PaymentDetails object from database if it exists. If not, create a
        # new object and set payment_detail_is_new to True
        self.payment_details = db_session.query(
            payment_details_class
        ).filter(payment_details_class.account_id == account_id).first()
        self.payment_detail_is_new = False
        if self.payment_details == None:
            self.payment_detail_is_new = True
            self.payment_details = payment_details_class()
            self.payment_details.account_id = account_id

    def dict_to_payment_details(self, payment_details_dict):
        self.payment_details.dict_to_values(payment_details_dict)
        return self.payment_details
