from flask.views import MethodView
from flask import Blueprint, request, jsonify, session

from project.server.models.tenancy import Tenancy, TenancyHistory
from project.server.models.tenant import Tenant
from project.server.models.payment_details import (CashDetails, PaypalDetails,
                                                   BankDetails)


tenancy_blueprint = Blueprint('tenancy', __name__)


class ListTenanciesAPI(MethodView):
    ''' Return list of tenancies belonging to user '''
    def get(self):
        return jsonify({'status': 'fail'}), 400


class AddTenancyAPI(MethodView):
    ''' Add New Tenancy '''
    def post(self):
        return jsonify({'status': 'fail'}), 400


class SaveTenancyNotesAPI(MethodView):
    ''' Save Tenancy Notes '''
    def post(self):
        return jsonify({'status': 'fail'}), 400


class SaveTenancyEndDateAPI(MethodView):
    ''' Save Tenancy Notes '''
    def post(self):
        return jsonify({'status': 'fail'}), 400


class GetTenancyAPI(MethodView):
    ''' Get Tenancy '''
    def post(self):
        return jsonify({'status': 'fail'}), 400


class DeleteTenancyAPI(MethodView):
    ''' Mark Tenancy as deleted '''
    def post(self):
        return jsonify({'status': 'fail'}), 400


# define the API resources
list_tenancies_view = ListTenanciesAPI.as_view('list_property')
add_tenancy_view = AddTenancyAPI.as_view('add_property')
get_tenancy_view = GetTenancyAPI.as_view('get_property')
save_tenancy_notes_view = SaveTenancyNotesAPI.as_view('save_tenancy_notes')
save_tenancy_enddate_view = SaveTenancyEndDateAPI.as_view(
    'save_tenancy_enddate'
)
delete_tenancy_view = DeleteTenancyAPI.as_view('delete_property')

# Add Rules for API Endpoints
tenancy_blueprint.add_url_rule(
    '/tenancy/list',
    view_func=list_tenancies_view,
    methods=['GET']
)
tenancy_blueprint.add_url_rule(
    '/tenancy/addnew',
    view_func=add_tenancy_view,
    methods=['POST']
)
tenancy_blueprint.add_url_rule(
    '/tenancy/get',
    view_func=get_tenancy_view,
    methods=['POST']
)
tenancy_blueprint.add_url_rule(
    '/tenancy/notes/save',
    view_func=save_tenancy_notes_view,
    methods=['POST']
)
tenancy_blueprint.add_url_rule(
    '/tenancy/enddate/save',
    view_func=save_tenancy_enddate_view,
    methods=['POST']
)
tenancy_blueprint.add_url_rule(
    '/tenancy/delete',
    view_func=delete_tenancy_view,
    methods=['POST']
)
