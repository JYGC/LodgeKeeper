'''
TenantBill and TenantBullHistory models and helper classes
'''

import calendar
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.ext.declarative import declared_attr

from project.server import db
from project.server import app
from project.server.models.tenancy import ITenancyId, ITenancyValues
from project.server.models.type_values import (TenantBillType, TenantBillStatus,
                                               PaymentTerms)


class ITenantBillValues():
    ''' Abstraction containing all columns for Tenant bill values '''
    @declared_attr
    def tenancy_id(self):
        return db.Column(db.Integer, db.ForeignKey('tenancy.id'),
                         nullable=False)
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
        self.date_created = datetime.now()
        self.is_deleted = False


class TenantBillHistory(db.Model, ITenantBillValues):
    ''' Model for managing Tenant Bill History data '''
    __tablename__ = 'tenant_bill_history'
    id = db.Column(db.Integer, primary_key=True)
    tenant_bill_id = db.Column(db.Integer, db.ForeignKey('tenant_bill.id'),
                               nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, updated_bill: (ITenantBillId, ITenantBillValues)=None):
        if updated_bill != None:
            self.tenant_bill_id = updated_bill.id
            self.tenancy_id = updated_bill.tenancy_id
            self.name = updated_bill.name
            self.notes = updated_bill.notes
            self.due_date = updated_bill.due_date
            self.tenant_bill_type_id = updated_bill.tenant_bill_type_id
            self.amount_total = updated_bill.amount_total
            self.amount_owing = updated_bill.amount_owing
            self.tenant_bill_status_id = updated_bill.tenant_bill_status_id
            self.is_deleted = updated_bill.is_deleted

        self.date_created = datetime.now()


class IRentScheduler():
    def __init__(self, tenancy: (ITenancyId, ITenancyValues)):
        self.tenant_bills = []
        self.next_due_date = None
        self._is_last_period = False

        self.tenancy = tenancy
        self.cur_due_date = tenancy.start_date
        self._set_next_due_date()
        self._set_for_next_period()
        self._create_tenant_bills()

    def _set_next_due_date(self):
        raise NotImplementedError
    
    def _set_for_next_period(self):
        if self.next_due_date >= self.tenancy.end_date:
            self._is_last_period = True
            self.next_due_date = self.tenancy.end_date
    
    def _compute_next_rent(self):
        return round((self.tenancy.rent_cost_per_week * (
            self.next_due_date - self.cur_due_date
        ).days / 7 if (self._is_last_period) else self.tenancy.rent_cost), 2)
    
    def _create_tenant_bill(self):
        tenant_bill = TenantBill()
        tenant_bill.tenancy_id = self.tenancy.id
        tenant_bill.name = 'Rent for ' + (self.tenancy.room_name if (
            self.tenancy.room_name != None
        ) else self.tenancy.address)
        tenant_bill.notes = 'For the period from %s to %s' % (
            self.cur_due_date.strftime(app.config['LETTER_DATE_FMT']),
            (self.next_due_date + timedelta(days=-1)).strftime(
                app.config['LETTER_DATE_FMT']
            )
        )
        tenant_bill.due_date = self.cur_due_date
        tenant_bill.tenant_bill_type_id = TenantBillType.get_value_id('rent')
        tenant_bill.amount_total = self._compute_next_rent()
        tenant_bill.amount_owing = tenant_bill.amount_total
        tenant_bill.tenant_bill_status_id = TenantBillStatus.get_value_id(
            'unpaid'
        )
        self.tenant_bills.append(tenant_bill)

    def _create_tenant_bills(self):
        while True:
            self._create_tenant_bill()
            if self._is_last_period:
                break
            else:
                self.cur_due_date = self.next_due_date
                self._set_next_due_date()
                self._set_for_next_period()


class IDayBasedScheduler(IRentScheduler):
    days_in_period = None

    def _set_next_due_date(self):
        self.next_due_date = self.cur_due_date + timedelta(
            days=self.days_in_period
        )


class MonthlyScheduler(IRentScheduler):
    def __init__(self, tenancy: (ITenancyId, ITenancyValues)):
        self.due_date_day = tenancy.start_date.day
        super().__init__(tenancy)

    def _set_next_due_date(self):
        next_due_yr_mth = datetime(self.cur_due_date.year, self.cur_due_date.month,
                              1) + relativedelta(months=1)
        max_cur_mth_max_days = calendar.monthrange(next_due_yr_mth.year,
                                                   next_due_yr_mth.month)[1]
        self.next_due_date = datetime(
            next_due_yr_mth.year,
            next_due_yr_mth.month,
            max_cur_mth_max_days if (
                self.due_date_day > max_cur_mth_max_days
            ) else self.due_date_day
        )


class FortnightlyScheduler(IDayBasedScheduler):
    days_in_period = 14


class WeeklyScheduler(IDayBasedScheduler):
    days_in_period = 7


class RentSchedulerSelector():
    def __init__(self, tenancy: (ITenancyId, ITenancyValues)):
        if PaymentTerms.type_values[
            tenancy.payment_terms_id
        ] == 'Per fortnight':
            self.bill_scheduler = FortnightlyScheduler(tenancy)
        elif PaymentTerms.type_values[tenancy.payment_terms_id] == 'Per week':
            self.bill_scheduler = WeeklyScheduler(tenancy)
        elif PaymentTerms.type_values[tenancy.payment_terms_id] == 'Per month':
            self.bill_scheduler = MonthlyScheduler(tenancy)
        else:
            raise Exception

    def get_tenant_bills(self):
        return self.bill_scheduler.tenant_bills
