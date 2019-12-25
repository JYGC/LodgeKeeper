from project.server import db
from project.server import app
from project.server.models.tenancy import Tenancy, TenancyHistory
from project.server.models.tenant import Tenant
from project.server.models.type_values import (PaymentMethod, PaymentTerms,
                                               RentType)


class ChkTenancyDbState():
    @classmethod
    def run(self, test_cls, test_values, **filter_values):
        tenancy_table = db.session.query(
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
        )
        tenancy_list = self.filter_query(tenancy_table, **filter_values).all()
        self.test_assersions(test_cls, tenancy_list, test_values,
                             **filter_values)
    
    @staticmethod
    def filter_query(tenancy_table, **filter_values):
        None
    
    @staticmethod
    def test_assersions(test_cls, tenancy_list, test_values, **filter_values):
        None


class ChkNoTenancyInDb(ChkTenancyDbState):
    @classmethod
    def run(self, test_cls, test_values):
        super().run(test_cls, test_values, **test_values)

    @staticmethod
    def filter_query(tenancy_table, **filter_values):
        return tenancy_table.filter(
            Tenancy.start_date == filter_values['start_date'],
            Tenancy.end_date == filter_values['end_date'],
            Tenancy.room_name == filter_values['room_name'],
            Tenancy.rent_cost == filter_values['rent_cost'],
            Tenancy.payment_description == filter_values['payment_description'],
            Tenancy.notes == filter_values['notes']
        )
    
    @staticmethod
    def test_assersions(test_cls, tenancy_list, test_values, **filter_values):
        test_cls.assertEqual(len(tenancy_list), 0)


class ChkTenancyDbStateById(ChkTenancyDbState):
    @staticmethod
    def filter_query(tenancy_table, **filter_values):
        return tenancy_table.filter(Tenancy.id == filter_values['tenancy_id'])
    
    @staticmethod
    def test_assersions(test_cls, tenancy_list, test_values, **filter_values):
        tenancy_id = filter_values['tenancy_id']
        test_cls.assertEqual(
            tenancy_list[0].Tenancy.end_date.strftime(app.config['DATE_FMT']),
            test_values['end_date']
        )
        test_cls.assertEqual(tenancy_list[0].Tenancy.address,
                             test_values['address'])
        test_cls.assertEqual(tenancy_list[0].RentType.value,
                             test_values['rent_type'])
        test_cls.assertEqual(tenancy_list[0].Tenancy.room_name,
                             test_values['room_name'])
        test_cls.assertEqual(tenancy_list[0].Tenancy.notes,
                             test_values['notes'])
        test_cls.assertEqual(tenancy_list[0].PaymentTerms.value,
                             test_values['payment_terms'])
        test_cls.assertEqual(
            tenancy_list[0].Tenancy.payment_description,
            test_values['payment_description']
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
            Tenant.tenancy_id == tenancy_id
        ).all()
        tenant_names = set(tenant.name for tenant in tenant_list)
        test_cls.assertEqual(set(test_values['tenants']) ^ tenant_names,
                             set())
