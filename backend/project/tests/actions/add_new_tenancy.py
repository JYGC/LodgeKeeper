import json
from datetime import datetime

from project.server import db
from project.server import app
from project.tests.base import BaseTestCase
from project.tests.actions.abcs import (IAction, IApiCheckAction,
                                        IDbCheckAction)
from project.tests.values.tenancy_values import NewTenancyValues
from project.server.models.type_values import (PaymentMethod, PaymentTerms,
                                               RentType)
from project.server.models.tenancy import Tenancy, TenancyHistory
from project.server.models.tenant import Tenant
from project.server.models.payment_details import (CashDetails, PaypalDetails,
                                                   BankDetails)


class AddTenancyApiAction():
    @staticmethod
    def run(test_cls, test_ntenancy_values, auth_token):
        ''' add tenancy via api '''
        return test_cls.client.post(
            '/tenancy/addnew',
            headers=dict(Authorization='Bearer ' + auth_token),
            data=json.dumps(dict(
                tenancy=test_ntenancy_values.tenancy.__dict__,
                tenants=test_ntenancy_values.tenants,
                notifications=test_ntenancy_values.notifications
            )),
            content_type='application/json',
        )


class ChkAddTenancyResponseAction():
    @staticmethod
    def run(test_cls, response):
        data = json.loads(response.data.decode())
        test_cls.assertEqual(data['status'], 'success')
        test_cls.assertIn('data', data)
        test_cls.assertTrue(data['data']['tenancy'][0]['id'])
        test_cls.assertEqual(response.content_type,
                             'application/json')
        test_cls.assertEqual(response.status_code, 201)


class ChkAddTenancyResponseActionBadRequest():
    @staticmethod
    def run(test_cls, response):
        data = json.loads(response.data.decode())
        test_cls.assertEqual(data['status'], 'fail')
        test_cls.assertEqual(response.content_type,
                                  'application/json')
        test_cls.assertEqual(response.status_code, 400)


class ChkAddTenancyResponseActionInvaildToken():
    @staticmethod
    def run(test_cls, response):
        data = json.loads(response.data.decode())
        test_cls.assertEqual(data['status'], 'fail')
        test_cls.assertNotIn('data', data)
        test_cls.assertEqual(data['message'],
                             'Invalid token. Please log in again.')
        test_cls.assertEqual(response.content_type,
                             'application/json')
        test_cls.assertEqual(response.status_code, 401)


class ChkAddTenancyDbStateAction():
    @staticmethod
    def run(test_cls, test_values, response):
        data = json.loads(response.data.decode())
        # Check tenancy tenancy history values and in database
        tenancy_list = db.session.query(
            Tenancy,
            TenancyHistory,
            RentType,
            PaymentTerms
        ).outerjoin(
            TenancyHistory,
            Tenancy.id == TenancyHistory.tenancy_id
        ).outerjoin(
            RentType,
            Tenancy.rent_type_id == RentType.id
        ).outerjoin(
            PaymentTerms,
            Tenancy.payment_terms_id == PaymentTerms.id
        ).filter(Tenancy.id == data['data']['tenancy'][0]['id']).all()
        test_cls.assertEqual(len(tenancy_list), 1)
        test_cls.assertEqual(
            tenancy_list[0].Tenancy.start_date.strftime(app.config['DATE_FMT']),
            test_values.tenancy.start_date
        )
        test_cls.assertEqual(
            tenancy_list[0].Tenancy.end_date.strftime(app.config['DATE_FMT']),
            test_values.tenancy.end_date
        )
        test_cls.assertEqual(tenancy_list[0].Tenancy.address,
                             test_values.tenancy.address)
        test_cls.assertEqual(tenancy_list[0].RentType.value,
                             test_values.tenancy.rent_type)
        test_cls.assertEqual(tenancy_list[0].Tenancy.room_name,
                             test_values.tenancy.room_name)
        test_cls.assertEqual(tenancy_list[0].Tenancy.notes,
                             test_values.tenancy.notes)
        test_cls.assertEqual(tenancy_list[0].PaymentTerms.value,
                             test_values.tenancy.payment_terms)
        test_cls.assertEqual(
            tenancy_list[0].Tenancy.payment_description,
            test_values.tenancy.payment_description
        )
        test_cls.assertEqual(tenancy_list[0].TenancyHistory.start_date,
                             tenancy_list[0].Tenancy.start_date)
        test_cls.assertEqual(tenancy_list[0].TenancyHistory.end_date,
                             tenancy_list[0].Tenancy.end_date)
        test_cls.assertEqual(tenancy_list[0].TenancyHistory.address,
                             tenancy_list[0].Tenancy.address)
        test_cls.assertEqual(tenancy_list[0].TenancyHistory.rent_type_id,
                             tenancy_list[0].Tenancy.rent_type_id)
        test_cls.assertEqual(tenancy_list[0].Tenancy.room_name,
                             tenancy_list[0].TenancyHistory.room_name)
        test_cls.assertEqual(tenancy_list[0].Tenancy.notes,
                             tenancy_list[0].TenancyHistory.notes)
        test_cls.assertEqual(
            tenancy_list[0].Tenancy.payment_terms_id,
            tenancy_list[0].TenancyHistory.payment_terms_id
        )
        test_cls.assertEqual(
            tenancy_list[0].Tenancy.payment_description,
            tenancy_list[0].TenancyHistory.payment_description
        )

        # Check tenant values in database
        tenant_list = db.session.query(Tenant).filter(
            Tenant.tenancy_id == data['data']['tenancy'][0]['id']
        ).all()
        tenant_names = {tenant.name for tenant in tenant_list}
        test_cls.assertEqual(set(test_values.tenants) ^ tenant_names,
                             set())
