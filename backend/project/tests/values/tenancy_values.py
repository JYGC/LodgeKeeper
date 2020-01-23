from typing import List
import datetime


NEW_TENANCY_LIST = [
    dict(
        start_date=(
            datetime.datetime.now() + datetime.timedelta(days=34)
        ).strftime("%Y-%m-%d"),
        end_date=(
            datetime.datetime.now() + datetime.timedelta(days=254)
        ).strftime("%Y-%m-%d"),
        address='123 Goldstern Drive, Tyron, QLD 5666',
        rent_type='Private Rooms',
        room_name='Room 4',
        notes=None,
        payment_terms='Per month',
        rent_cost=865.99,
        payment_description='Pay this is Account A',
        tenants=['James Balls', 'Helena Coltis'],
        notifications=[7, 14]
    ),
    dict(
        start_date=(
            datetime.datetime.now() - datetime.timedelta(days=1000)
        ).strftime("%Y-%m-%d"),
        end_date=(
            datetime.datetime.now() + datetime.timedelta(days=2994)
        ).strftime("%Y-%m-%d"),
        address='123 Goldstern Drive, Tyron, QLD 5666',
        rent_type='Whole Property',
        room_name=None,
        notes=None,
        payment_terms='Per week',
        rent_cost=400.77,
        payment_description='Pay this is Account A',
        tenants=['Xue Yang', 'Gladis Vue'],
        notifications=[2, 5, 10, 14]
    ),
    dict(
        start_date=(
            datetime.datetime.now() - datetime.timedelta(days=3000)
        ).strftime("%Y-%m-%d"),
        end_date=(
            datetime.datetime.now() - datetime.timedelta(days=2000)
        ).strftime("%Y-%m-%d"),
        address='123 Goldstern Drive, Tyron, QLD 5666',
        rent_type='Private Rooms',
        room_name='Room 4',
        notes=None,
        payment_terms='Per month',
        rent_cost=865.99,
        payment_description='Pay this is Account A',
        tenants=['Sally Vegus'],
        notifications=[16]
    ),
    dict(
        start_date=(
            datetime.datetime.now() + datetime.timedelta(days=0)
        ).strftime("%Y-%m-%d"),
        end_date=(
            datetime.datetime.now() + datetime.timedelta(days=1254)
        ).strftime("%Y-%m-%d"),
        address='123 Ternstein Drive, Tyron, QLD 5666',
        rent_type='Private Rooms',
        room_name='Room 2',
        notes=None,
        payment_terms='Per fortnight',
        rent_cost=706.99,
        payment_description='Pay this is Account A TEST TEST',
        tenants=['Larry Kettelmann', 'Lousie Kettelmann', 'Jim Kettlemann'],
        notifications=[3, 4]
    ),
    dict(
        start_date=(
            datetime.datetime.now() + datetime.timedelta(days=0)
        ).strftime("%Y-%m-%d"),
        end_date=(
            datetime.datetime.now() + datetime.timedelta(days=9254)
        ).strftime("%Y-%m-%d"),
        address='123 Ternstein Drive, Tyron, QLD 5666',
        rent_type='Whole Property',
        room_name=None,
        notes=None,
        payment_terms='Per fortnight',
        rent_cost=706.99,
        payment_description='Pay this is Account A TEST TEST',
        tenants=['Peson KettA', 'Peson KettB', 'Peson KettC', 'Peson KettD',
                 'Peson KettF'],
        notifications=[1, 2, 4, 3]
    )
]

NEW_PRIVATE_ROOM = dict(
    start_date=(
        datetime.datetime.now() + datetime.timedelta(days=34)
    ).strftime("%Y-%m-%d"),
    end_date=(
        datetime.datetime.now() + datetime.timedelta(days=254)
    ).strftime("%Y-%m-%d"),
    address='123 Goldstern Drive, Tyron, QLD 5666',
    rent_type='Private Rooms',
    room_name='Room 4',
    notes=None,
    payment_terms='Per month',
    rent_cost=865.99,
    payment_description='Pay this is Account A',
    tenants=['James Balls', 'Helena Colts'],
    notifications=[3, 4]
)

NEW_WHOLE_PROPERTY = dict(
    NEW_PRIVATE_ROOM,
    room_name=None,
    rent_type='Whole Property',
    rent_cost=1999.99
)

PRIVATE_ROOM_BAD_TYPES = dict(
    start_date=(
        datetime.datetime.now() + datetime.timedelta(days=34)
    ).strftime("%Y-%m-%d"),
    end_date=(
        datetime.datetime.now() + datetime.timedelta(days=254)
    ).strftime("%Y-%m-%d"),
    address='123 Goldstern Drive, Tyron, QLD 5666',
    rent_type='Room Private',
    room_name='Room 4',
    notes=None,
    payment_terms='Per month',
    rent_cost=865.99,
    payment_description='Pay this is Account A',
    tenants=['James Balls', 'Helena Colts'],
    notifications=[3, 4]
)

PRIVATE_ROOM_NO_TENANTS = dict(
    NEW_PRIVATE_ROOM,
    tenants=[]
)

WHOLE_PROPERTY_NO_TENANTS = dict(
    PRIVATE_ROOM_NO_TENANTS,
    rent_type='Whole Property'
)

PRIVATE_ROOM_NO_NOTIFICATIONS = dict(
    NEW_PRIVATE_ROOM,
    tenants=[]
)

WHOLE_PROPERTY_NO_NOTIFICATIONS = dict(
    PRIVATE_ROOM_NO_NOTIFICATIONS,
    rent_type='Whole Property'
)

PRIVATE_ROOM_NO_TENANTS_NOTIFICATIONS = dict(
    NEW_PRIVATE_ROOM,
    tenants=[],
    notifications=[]
)

WHOLE_PROPERTY_NO_TENANTS_NOTIFICATIONS = dict(
    PRIVATE_ROOM_NO_TENANTS_NOTIFICATIONS,
    rent_type='Whole Property'
)

UNSTARTED_PRIVATE_ROOM_TENANCY = dict(
    start_date=(
        datetime.datetime.now() + datetime.timedelta(days=34)
    ).strftime("%Y-%m-%d"),
    end_date=(
        datetime.datetime.now() + datetime.timedelta(days=454)
    ).strftime("%Y-%m-%d"),
    address='123 Goldstern Drive, Tyron, QLD 5666',
    rent_type='Private Rooms',
    room_name='Room 4',
    notes='I was walking do a street one night and got my face kicked in. I thought I deserved it',
    payment_terms='Per month',
    rent_cost=865.99,
    payment_description='Pay this is Account A',
    tenants=['Rachel Sackler', 'David Sackler'],
    notifications=[2,3,4,5]
)
UNSTARTED_PRIVATE_ROOM_TENANCY_NO_ROOM_NAME = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    room_name=None
)
UNSTARTED_PRIVATE_ROOM_TENANCY_CHANGE_ADDRESS = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    address='54 Green Drive, Tyron, QLD 5666'
)
UNSTARTED_PRIVATE_ROOM_TENANCY_NO_ADDRESS = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    address=''
)
UNSTARTED_PRIVATE_ROOM_TENANCY_NULL_ADDRESS = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    address=None
)
UNSTARTED_WHOLE_PROPERTY_TENANCY = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    rent_type='Whole Property',
    room_name=''
)
UNSTARTED_WHOLE_PROPERTY_TENANCY_NULL_ROOM_NAME = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    rent_type='Whole Property',
    room_name=None
)
UNSTARTED_TENANCY_NO_RENT_TYPE = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    rent_type=''
)
UNSTARTED_TENANCY_NULL_RENT_TYPE = dict(
    UNSTARTED_PRIVATE_ROOM_TENANCY,
    rent_type=''
)
