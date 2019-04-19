import datetime
from sqlalchemy.ext.declarative import declared_attr

from project.server import db


class ITenantBillValues():
    ''' Abstraction containing all columns for Tenant bill values '''
    name = db.Column(db.String(256))
    notes = db.Column(db.Text)
    due_date = db.Column(db.DateTime, nullable=False)
    @declared_attr
    def tenant_bill_type_id(self):
        return db.Column(db.Integer, db.ForeignKey('tenant_bill_type.id'),
                         nullable=False)
    amount_total = db.Column(db.Numeric(16, 2), nullable=False)
    amount_owing = db.Column(db.Numeric(16, 2), nullable=False)
    @declared_attr
    def tenant_bill_status_id(self):
        return db.Column(db.Integer, db.ForeignKey('tenant_bill_status.id'),
                         nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)


class ITenantBillId():
    ''' Abstraction containing Tenanct bill Id '''
    id = db.Column(db.Integer, primary_key=True)


class TenantBill(db.Model, ITenantBillId, ITenantBillValues):
    ''' Model to manage Tenant data '''
    __tablename__ = 'tenant_bill'
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.date_created = datetime.datetime.now()
        self.is_deleted = False


class TenantBillHistory(db.Model, ITenantBillValues):
    ''' Model for managing Tenant Bill History data '''
    __tablename__ = 'tenant_bill_history'
    id = db.Column(db.Integer, primary_key=True)
    tenant_bill_id = db.Column(db.Integer, db.ForeignKey('tenancy.id'),
                               nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, updated_bill: (ITenantBillId, ITenantBillValues)=None):
        if updated_bill != None:
            self.name = updated_bill.name
            self.notes = updated_bill.notes
            self.due_date = updated_bill.due_date
            self.tenant_bill_type_id = updated_bill.tenant_bill_type_id
            self.amount_total = updated_bill.amount_total
            self.amount_owing = updated_bill.amount_owing
            self.tenant_bill_status_id = updated_bill.tenant_bill_status_id
            self.is_deleted = updated_bill.is_deleted

        self.date_created = datetime.datetime.now()
