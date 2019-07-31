'''
Tenancy and TenancyHistory models
'''

import datetime
from sqlalchemy.ext.declarative import declared_attr

from project.server import db
from project.server.models.type_values import PaymentTerms


class ITenancyValues():
    ''' Abstraction containing all columns for Tenancy details '''
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    address = db.Column(db.String(512), nullable=False)
    room_name = db.Column(db.String(256))
    @declared_attr
    def rent_type_id(self):
        return db.Column(db.Integer, db.ForeignKey('rent_type.id'),
                         nullable=False)
    @declared_attr
    def payment_terms_id(self):
        return db.Column(db.Integer, db.ForeignKey('payment_terms.id'),
                         nullable=False)
    rent_cost = db.Column(db.Numeric(16, 2), nullable=False)
    rent_cost_per_week = db.Column(db.Numeric(16, 2), nullable=False)
    @declared_attr
    def payment_method_id(self):
        return db.Column(db.Integer, db.ForeignKey('payment_method.id'),
                         nullable=False)
    notes = db.Column(db.Text)
    is_deleted = db.Column(db.Boolean, nullable=False)
    @declared_attr
    def account_id(self):
        return db.Column(db.Integer, db.ForeignKey('account.id'),
                         nullable=False)


class ITenancyId():
    ''' Abstraction containing Tenancy Id '''
    id = db.Column(db.Integer, primary_key=True)


class Tenancy(db.Model, ITenancyId, ITenancyValues):
    ''' Model for managing Tenancy data '''
    __tablename__ = 'tenancy'
    date_created = db.Column(db.DateTime, nullable=False)

    def set_rent_cost(self, rent_cost, payment_terms_id):
        self.rent_cost = rent_cost
        self.payment_terms_id = payment_terms_id
        if PaymentTerms.type_values[payment_terms_id] == 'Per month':
            self.rent_cost_per_week = round(rent_cost * 12 * 7 / 365, 2)
        elif PaymentTerms.type_values[payment_terms_id] == 'Per fortnight':
            self.rent_cost_per_week = round(rent_cost * 7 / 14, 2)
        elif PaymentTerms.type_values[payment_terms_id] == 'Per week':
            self.rent_cost_per_week = rent_cost

    def __init__(self):
        self.date_created = datetime.datetime.now()
        self.is_deleted = False


class TenancyHistory(db.Model, ITenancyValues):
    ''' Model for managing Tenancy History data '''
    __tablename__ = 'tenancy_history'
    id = db.Column(db.Integer, primary_key=True)
    tenancy_id = db.Column(db.Integer, db.ForeignKey('tenancy.id'),
                           nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, updated_tenancy: (ITenancyId, ITenancyValues)=None):
        if updated_tenancy != None:
            self.tenancy_id = updated_tenancy.id
            self.start_date = updated_tenancy.start_date
            self.end_date = updated_tenancy.end_date
            self.address = updated_tenancy.address
            self.room_name = updated_tenancy.room_name
            self.rent_type_id = updated_tenancy.rent_type_id
            self.payment_terms_id = updated_tenancy.payment_terms_id
            self.rent_cost = updated_tenancy.rent_cost
            self.rent_cost_per_week = updated_tenancy.rent_cost_per_week
            self.payment_method_id = updated_tenancy.payment_method_id
            self.notes = updated_tenancy.notes
            self.is_deleted = updated_tenancy.is_deleted
            self.account_id = updated_tenancy.account_id

        self.date_created = datetime.datetime.now()
