from flask.views import MethodView
from flask import Blueprint

from project.server.models.tenant_bill import TenantBill, TenantBillHistory


tenant_bill_blueprint = Blueprint('tenant_bill', __name__)


class ListTenantBillsAPI(MethodView):
    ''' Return all user's tenant bills '''
    def get(self):
        return False, 400


class AddTenantBillAPI(MethodView):
    ''' Add tenant bills '''
    def post(self):
        return False, 400


class SaveTenantBillAPI(MethodView):
    ''' Save tenant bills '''
    def post(self):
        return False, 400


class DeleteTenantBillAPI(MethodView):
    ''' Delete tenant bills '''
    def post(self):
        return False, 400


# define the API resources
list_tenant_bills_view = ListTenantBillsAPI.as_view('list_tenant_bills')
add_tenant_bill_view = AddTenantBillAPI.as_view('add_tenant_bill')
save_tenant_bill_view = SaveTenantBillAPI.as_view('save_tenant_bill')
delete_tenant_bill_view = DeleteTenantBillAPI.as_view('delete_tenant_bill')

# Add Rules for API Endpoints
tenant_bill_blueprint.add_url_rule(
    '/tenantbill/list',
    view_func=list_tenant_bills_view,
    methods=['GET']
)
tenant_bill_blueprint.add_url_rule(
    '/tenantbill/add',
    view_func=add_tenant_bill_view,
    methods=['POST']
)
tenant_bill_blueprint.add_url_rule(
    '/tenantbill/save',
    view_func=save_tenant_bill_view,
    methods=['POST']
)
tenant_bill_blueprint.add_url_rule(
    '/tenantbill/delete',
    view_func=delete_tenant_bill_view,
    methods=['POST']
)
