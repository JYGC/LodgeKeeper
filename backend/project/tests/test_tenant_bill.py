# import sys
# sys.path.insert(0, '/home/junying/Desktop/LodgeKeeper/backend')
# from datetime import datetime

# from project.server.models.tenant_bill import RentSchedulerSelector
# from project.server.models.tenancy import Tenancy
# from project.server.models.type_values import (RentType, PaymentTerms,
#                                                PaymentMethod)

# tenancy = Tenancy()
# tenancy.id = 1
# tenancy.start_date = datetime(2019, 1, 31)
# tenancy.end_date = datetime(2019, 3, 29)
# tenancy.address = '345 Gab Street, North Baland, QLD 4555'
# tenancy.room_name = 'Test 1'
# tenancy.rent_type_id = 2
# tenancy.set_rent_cost(200, 1)
# tenancy.payment_method_id = 2
# tenancy.notes = 'test'
# tenancy.account_id = 1

# tenant_bill_selector = RentSchedulerSelector(tenancy)

# for obj in tenant_bill_selector.get_tenant_bills():
#     print(obj.date_created)

# print('====================')

# tenancy = Tenancy()
# tenancy.id = 2
# tenancy.start_date = datetime(2019, 1, 31)
# tenancy.end_date = datetime(2019, 3, 29)
# tenancy.address = '345 Gab Street, North Baland, QLD 4555'
# tenancy.room_name = 'Test 1'
# tenancy.rent_type_id = 2
# tenancy.set_rent_cost(200, 1)
# tenancy.payment_method_id = 2
# tenancy.notes = 'test'
# tenancy.account_id = 1

# tenant_bill_selector = RentSchedulerSelector(tenancy)

# for obj in tenant_bill_selector.get_tenant_bills():
#     print(obj.date_created)