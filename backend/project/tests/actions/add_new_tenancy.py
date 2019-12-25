import json
from datetime import datetime

from project.server import db
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.actions.response_handling import ChkSuccessfulModelResponse
from project.server.models.type_values import (PaymentMethod, PaymentTerms,
                                               RentType)
from project.server.models.tenancy import Tenancy, TenancyHistory
from project.server.models.tenant import Tenant
from project.server.models.payment_details import (CashDetails, PaypalDetails,
                                                   BankDetails)


class AddTenancyApiAction():
    @staticmethod
    def run(test_cls, tenancy_values, auth_token):
        ''' add tenancy via api '''
        return test_cls.client.post(
            '/tenancy/addnew',
            headers=dict(Authorization='Bearer ' + auth_token),
            data=json.dumps(dict(
                tenancy=dict(
                    start_date=tenancy_values['start_date'],
                    end_date=tenancy_values['end_date'],
                    address=tenancy_values['address'],
                    rent_type=tenancy_values['rent_type'],
                    room_name=tenancy_values['room_name'],
                    payment_terms=tenancy_values['payment_terms'],
                    rent_cost=tenancy_values['rent_cost'],
                    payment_description=tenancy_values['payment_description'],
                ),
                tenants=tenancy_values['tenants'],
                notifications=tenancy_values['notifications']
            )),
            content_type='application/json',
        )


class ChkAddTenancyResponseAction(ChkSuccessfulModelResponse):
    _id_key = 'tenancy_id'
    _resp_code = 201
    