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


class AddNewTenancy(IAction, IApiCheckAction, IDbCheckAction):
    ''' Add new tenancy '''
    # Variables for use
    auth_token = None
    test_values = None
    
    # Variables to store api reponse data
    response = None
    data = None

    def __init__(self, test_cls: BaseTestCase):
        super().__init__(test_cls)
    
    def api_request(self):
        ''' add tenancy via api '''
        self.response = self.test_cls.client.post(
            '/tenancy/addnew',
            headers=dict(Authorization='Bearer ' + self.auth_token),
            data=json.dumps(dict(
                tenancy=self.test_values.tenancy.__dict__,
                tenants=self.test_values.tenants,
                payment_details=self.test_values.payment_details.__dict__,
                notifications=self.test_values.notifications
            )),
            content_type='application/json',
        )

    def run(self, auth_token, test_values: NewTenancyValues):
        ''' run action '''
        self.auth_token = auth_token
        self.test_values = test_values

        self.api_request()
        self.data = json.loads(self.response.data.decode())
        self.check_response()
        self.check_db_state()
        return self.data

    def check_response(self):
        self.test_cls.assertEqual(self.data['status'], 'success')
        self.test_cls.assertIn('data', self.data)
        self.test_cls.assertTrue(self.data['data']['tenancy'][0]['id'])
        self.test_cls.assertEqual(self.response.content_type,
                                  'application/json')
        self.test_cls.assertEqual(self.response.status_code, 201)

    def check_db_state(self):
        # Check tenancy tenancy history values and in database
        tenancy_list = db.session.query(
            Tenancy,
            TenancyHistory,
            RentType,
            PaymentTerms,
            PaymentMethod
        ).outerjoin(
            TenancyHistory,
            Tenancy.id == TenancyHistory.tenancy_id
        ).outerjoin(
            RentType,
            Tenancy.rent_type_id == RentType.id
        ).outerjoin(
            PaymentTerms,
            Tenancy.payment_terms_id == PaymentTerms.id
        ).outerjoin(
            PaymentMethod,
            Tenancy.payment_method_id == PaymentMethod.id
        ).filter(Tenancy.id == self.data['data']['tenancy'][0]['id']).all()
        self.test_cls.assertEqual(len(tenancy_list), 1)
        self.test_cls.assertEqual(
            tenancy_list[0].Tenancy.start_date.strftime(app.config['DATE_FMT']),
            self.test_values.tenancy.start_date
        )
        self.test_cls.assertEqual(
            tenancy_list[0].Tenancy.end_date.strftime(app.config['DATE_FMT']),
            self.test_values.tenancy.end_date
        )
        self.test_cls.assertEqual(tenancy_list[0].Tenancy.address,
                                  self.test_values.tenancy.address)
        self.test_cls.assertEqual(tenancy_list[0].RentType.value,
                                  self.test_values.tenancy.rent_type)
        self.test_cls.assertEqual(tenancy_list[0].Tenancy.room_name,
                                  self.test_values.tenancy.room_name)
        self.test_cls.assertEqual(tenancy_list[0].Tenancy.notes,
                                  self.test_values.tenancy.notes)
        self.test_cls.assertEqual(tenancy_list[0].PaymentTerms.value,
                                  self.test_values.tenancy.payment_terms)
        self.test_cls.assertEqual(
            tenancy_list[0].PaymentMethod.value,
            self.test_values.payment_details.payment_method
        )
        self.test_cls.assertEqual(tenancy_list[0].TenancyHistory.start_date,
                                  tenancy_list[0].Tenancy.start_date)
        self.test_cls.assertEqual(tenancy_list[0].TenancyHistory.end_date,
                                  tenancy_list[0].Tenancy.end_date)
        self.test_cls.assertEqual(tenancy_list[0].TenancyHistory.address,
                                  tenancy_list[0].Tenancy.address)
        self.test_cls.assertEqual(tenancy_list[0].TenancyHistory.rent_type_id,
                                  tenancy_list[0].Tenancy.rent_type_id)
        self.test_cls.assertEqual(tenancy_list[0].Tenancy.room_name,
                                  tenancy_list[0].TenancyHistory.room_name)
        self.test_cls.assertEqual(tenancy_list[0].Tenancy.notes,
                                  tenancy_list[0].TenancyHistory.notes)
        self.test_cls.assertEqual(
            tenancy_list[0].Tenancy.payment_terms_id,
            tenancy_list[0].TenancyHistory.payment_terms_id
        )
        self.test_cls.assertEqual(
            tenancy_list[0].Tenancy.payment_method_id,
            tenancy_list[0].TenancyHistory.payment_method_id
        )

        # Check tenant values in database
        tenant_list = db.session.query(Tenant).filter(
            Tenant.tenancy_id == self.data['data']['tenancy'][0]['id']
        ).all()
        tenant_names = {tenant.name for tenant in tenant_list}
        self.test_cls.assertEqual(set(self.test_values.tenants) ^ tenant_names,
                                  set())

        self.account_id = tenancy_list[0].Tenancy.account_id
        self.check_payment_details_in_db()

    def check_payment_details_in_db(self):
        pass


class AddNewTenancyWithCashDetails(AddNewTenancy):
    ''' Add new tenancy with new cash payment details '''
    def check_payment_details_in_db(self):
        payment_details = db.session.query(
            CashDetails
        ).filter(CashDetails.account_id == self.account_id).all()
        self.test_cls.assertEqual(len(payment_details), 1)
        self.test_cls.assertEqual(
            payment_details[0].description,
            self.test_values.payment_details.description
        )


class AddNewTenancyWithPaypalDetails(AddNewTenancy):
    ''' Add new tenancy with new cash payment details '''
    def check_payment_details_in_db(self):
        payment_details = db.session.query(
            PaypalDetails
        ).filter(PaypalDetails.account_id == self.account_id).all()
        self.test_cls.assertEqual(len(payment_details), 1)
        self.test_cls.assertEqual(
            payment_details[0].description,
            self.test_values.payment_details.description
        )
        self.test_cls.assertEqual(payment_details[0].email,
                                  self.test_values.payment_details.email)
        self.test_cls.assertEqual(payment_details[0].reason,
                                  self.test_values.payment_details.reason)
        self.test_cls.assertEqual(payment_details[0].message,
                                  self.test_values.payment_details.message)


class AddNewTenancyWithBankDetails(AddNewTenancy):
    ''' Add new tenancy with new bank transfer details '''
    def check_payment_details_in_db(self):
        payment_details = db.session.query(
            BankDetails
        ).filter(BankDetails.account_id == self.account_id).all()
        self.test_cls.assertEqual(len(payment_details), 1)
        self.test_cls.assertEqual(
            payment_details[0].description,
            self.test_values.payment_details.description
        )
        self.test_cls.assertEqual(payment_details[0].bank_name,
                                  self.test_values.payment_details.bank_name)
        self.test_cls.assertEqual(payment_details[0].account_name,
                                  self.test_values.payment_details.account_name)
        self.test_cls.assertEqual(payment_details[0].bsb_number,
                                  self.test_values.payment_details.bsb_number)
        self.test_cls.assertEqual(
            payment_details[0].account_number,
            self.test_values.payment_details.account_number
        )


class AddNewTenancyBadRequest(AddNewTenancy):
    ''' Add new tenancy with unrecognised value types '''
    def check_response(self):
        self.test_cls.assertEqual(self.data['status'], 'fail')
        self.test_cls.assertEqual(self.response.content_type,
                                  'application/json')
        self.test_cls.assertEqual(self.response.status_code, 401)
    
    def check_db_state(self):
        pass


class AddNewTenancyInvalidAuthentication(AddNewTenancy):
    ''' Add new tenancy with invalid authenication '''
    def check_response(self):
        self.test_cls.assertEqual(self.data['status'], 'fail')
        self.test_cls.assertNotIn('data', self.data)
        self.test_cls.assertEqual(self.data['message'],
                                  'Invalid token. Please log in again.')
        self.test_cls.assertEqual(self.response.content_type,
                                  'application/json')
        self.test_cls.assertEqual(self.response.status_code, 401)
    
    def check_db_state(self):
        pass
        