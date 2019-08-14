from typing import List

from .payment_details_values import (IPaymentDetails, CashDetails,
                                     PayPalDetails, BankDetails)


class TenancyValues():
    def __init__(self, start_date=None, end_date=None, address=None,
                 rent_type=None, room_name=None, notes=None,
                 payment_terms=None, rent_cost=None, payment_description=None):
        self.start_date = start_date
        self.end_date = end_date
        self.address = address
        self.rent_type = rent_type
        self.room_name = room_name
        self.notes = notes
        self.payment_terms = payment_terms
        self.rent_cost = rent_cost
        self.payment_description = payment_description


class NewTenancyValues():
    def __init__(self, tenancy_values: TenancyValues=None,
                 tenant_list: List[str]=None,
                 notification_list: List[int]=None):
        self.tenancy = tenancy_values
        self.tenants = tenant_list
        self.notifications = notification_list


import datetime

test_new_tenancy_values = {
    'all_details': NewTenancyValues(
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
            payment_terms='Per month',
            rent_cost=865.99,
            payment_description='Pay this is Account A'
        ),
        ['James Balls', 'Helena Colts'],
        [3, 4]
    ),
    'with_cash': NewTenancyValues(
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
            payment_terms='Per month',
            rent_cost=865.99,
            payment_description='Pay this is Account A'
        ),
        ['James Balls', 'Helena Colts'],
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
            payment_terms='Per month',
            rent_cost=865.99,
            payment_description='Pay this is Account A'
        ),
        ['James Balls', 'Helena Colts'],
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
            payment_terms='Per month',
            rent_cost=865.99,
            payment_description='Pay this is Account A'
        ),
        ['James Balls', 'Helena Colts'],
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
            payment_terms='Per month',
            rent_cost=865.99,
            payment_description='Pay this is Account A'
        ),
        ['James Balls', 'Helena Colts'],
        [3, 4]
    )
}