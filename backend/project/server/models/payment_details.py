from sqlalchemy.ext.declarative import declared_attr

from project.server import db

class IPaymentDetails():
    ''' Payment detils abstraction '''
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.Text)
    @declared_attr
    def account_id(self):
        return db.Column(db.Integer, db.ForeignKey('account.id'),
                         nullable=False)


class CashDetails(db.Model, IPaymentDetails):
    ''' Model for Cash payment details '''
    __tablename__ = 'cash_details'
    pass


class PaypalDetails(db.Model, IPaymentDetails):
    ''' Model for paypal details '''
    __tablename__ = 'paypal_details'
    email = db.Column(db.String(255))
    reason = db.Column(db.String(1024))
    message = db.Column(db.String(1024))


class BankTransferDetails(db.Model, IPaymentDetails):
    ''' Model for bank details '''
    __tablename__ = 'bank_transfer_details'
    bank_name = db.Column(db.String(255))
    account_number = db.Column(db.String(255))
    bsb_number = db.Column(db.String(7))
    account_number = db.Column(db.String(255))
