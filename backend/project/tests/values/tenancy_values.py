from typing import List

from .payment_details import (IPaymentDetails, CashDetails, PayPalDetails,
                              BankTransfer)


class TenancyValues():
    def __init__(self, start_date=None, end_date=None, address=None,
                 rent_type=None, room_name=None, notes=None,
                 payment_terms=None):
        self.start_date = start_date
        self.end_date = end_date
        self.address = address
        self.rent_type = rent_type
        self.room_name = room_name
        self.notes = notes
        self.payment_terms = payment_terms


class NewTenancyValues():
    def __init__(self, tenancy_values: TenancyValues=None,
                 tenant_list: List[str]=None,
                 payment_details: IPaymentDetails=None,
                 notification_list: List[int]=None):
        self.tenancy = tenancy_values
        self.tenants = tenant_list
        self.payment_details = payment_details
        self.notifications = notification_list


import datetime

test_new_tenancy_values = {
    'with_cash': NewTenancyValues(
        TenancyValues(
            start_date=(
                datetime.datetime.now() + datetime.timedelta(days=34)
            ).strftime("%Y-%m-%d"),
            end_date=(
                datetime.datetime.now() + datetime.timedelta(days=254)
            ).strftime("%Y-%m-%d"),
            address='123 Goldstern Drive, Tyron, QLD 5666',
            rent_type='Private Rooms', room_name='Room 4',
            payment_terms='Monthly'
        ),
        ['James Balls', 'Helena Colts'],
        CashDetails('Payment for rent Balls and colt'),
        [3, 4]
    ),
    'with_paypal': NewTenancyValues(
        TenancyValues(
            start_date=(
                datetime.datetime.now() + datetime.timedelta(days=34)
            ).strftime("%Y-%m-%d"),
            end_date=(
                datetime.datetime.now() + datetime.timedelta(days=254)
            ).strftime("%Y-%m-%d"),
            address='123 Goldstern Drive, Tyron, QLD 5666',
            rent_type='Private Rooms',
            room_name='Room 4',
            payment_terms='Monthly'
        ),
        ['James Balls', 'Helena Colts'],
        PayPalDetails(description='Payment for rent Balls and colt',
                      paypal_email='jamesballs@hotmail.com',
                      reason='Rent Payment', message='Payment rent'),
        [3, 4]
    ),
    'with_bank_transfer': NewTenancyValues(
        TenancyValues(
            start_date=(
                datetime.datetime.now() + datetime.timedelta(days=34)
            ).strftime("%Y-%m-%d"),
            end_date=(
                datetime.datetime.now() + datetime.timedelta(days=254)
            ).strftime("%Y-%m-%d"),
            address='123 Goldstern Drive, Tyron, QLD 5666',
            rent_type='Private Rooms',
            room_name='Room 4',
            payment_terms='Monthly'
        ),
        ['James Balls', 'Helena Colts'],
        BankTransfer(description='Payment for rent Balls and colt',
                     bank_name='Duetches Limited', account_name='Rogay Peirius',
                     bsb_number='345876', account_number='1236843023'),
        [3, 4]
    ),
    'with_bad_types': NewTenancyValues(
        TenancyValues(
            start_date=(
                datetime.datetime.now() + datetime.timedelta(days=34)
            ).strftime("%Y-%m-%d"),
            end_date=(
                datetime.datetime.now() + datetime.timedelta(days=254)
            ).strftime("%Y-%m-%d"),
            address='123 Goldstern Drive, Tyron, QLD 5666',
            rent_type='Room Private',
            room_name='Room 4',
            payment_terms='Month'
        ),
        ['James Balls', 'Helena Colts'],
        CashDetails('Payment for rent Balls and colt'),
        [3, 4]
    )
}