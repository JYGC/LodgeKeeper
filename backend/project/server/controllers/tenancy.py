'''
All API endpoints that handle tenancy entities and actions
'''

import traceback
from datetime import datetime
from flask.views import MethodView
from flask import Blueprint, request, jsonify, session
from sqlalchemy import and_

from project.server import db
from project.server import app
from project.server.models.auth import User
from project.server.models.tenancy import Tenancy, TenancyHistory
from project.server.models.tenant import Tenant
from project.server.models.payment_details import PaymentDetailsPresenter
from project.server.models.notifications import Notification
from project.server.models.tenant_bill import (RentSchedulerSelector,
                                               TenantBill,
                                               TenantBillHistory)
from project.server.models.type_values import (RentType, PaymentTerms,
                                               PaymentMethod)


UNKNOWN_ITEM_TYPE = 'Payment type or Rent type unknown'


tenancy_blueprint = Blueprint('tenancy', __name__)


class ListTenanciesAPI(MethodView):
    ''' Return list of tenancies belonging to user '''
    def get(self):
        ''' PROCESS GET REQUEST '''
        return jsonify({'status': 'fail'}), 400


class AddNewTenancyAPI(MethodView):
    ''' Add New Tenancy '''
    def post(self):
        '''
        Add new tenancy, tenants, notifications, tenant_bills to database.
        Returns 400 if there is an error.
        '''
        try:
            if not request.is_json:
                raise Exception
            self.request_json = request.get_json()

            # Get required foriegn keys. If not successful, throw error
            foreign_ids_set = db.session.query(
                User.account_id,
                RentType.id,
                PaymentTerms.id,
                PaymentMethod.id
            ).filter(
                User.id == int(session.pop('user_id', None))
            ).filter(
                RentType.value == self.request_json['tenancy']['rent_type']
            ).filter(
                PaymentTerms.value == self.request_json['tenancy'][
                    'payment_terms'
                ]
            ).filter(
                PaymentMethod.value == self.request_json['payment_details'][
                    'payment_method'
                ]
            ).first()
            if foreign_ids_set == None or None in foreign_ids_set:
                self.response = jsonify({
                    'status': 'fail',
                    'message': UNKNOWN_ITEM_TYPE
                }), 400
            self.foriegn_ids = {
                'user_account_id': foreign_ids_set[0],
                'rent_type_id': foreign_ids_set[1],
                'payment_terms_id': foreign_ids_set[2],
                'payment_method_id': foreign_ids_set[3]
            }

            # Add Tenancy and TenancyHistory to database
            new_tenancy = Tenancy()
            new_tenancy.start_date = datetime.strptime(
                self.request_json['tenancy']['start_date'],
                app.config['DATE_FMT']
            )
            new_tenancy.end_date = datetime.strptime(
                self.request_json['tenancy']['end_date'],
                app.config['DATE_FMT']
            )
            new_tenancy.address = self.request_json['tenancy']['address']
            new_tenancy.room_name = self.request_json['tenancy']['room_name']
            new_tenancy.rent_type_id = self.foriegn_ids['rent_type_id']
            new_tenancy.set_rent_cost(
                round(float(self.request_json['tenancy']['rent_cost']), 2),
                self.foriegn_ids['payment_terms_id']
            )
            new_tenancy.payment_method_id = self.foriegn_ids[
                'payment_method_id'
            ]
            new_tenancy.notes = self.request_json['tenancy']['notes']
            new_tenancy.account_id = self.foriegn_ids['user_account_id']
            db.session.add(new_tenancy)
            db.session.flush()
            db.session.add(TenancyHistory(updated_tenancy=new_tenancy))

            # Add Tenants to database
            db.session.bulk_save_objects([Tenant(
                tenant_name,
                new_tenancy.id
            ) for tenant_name in self.request_json['tenants']])

            # Update or create account payment details
            pd_presenter = PaymentDetailsPresenter(
                db.session,
                self.request_json['payment_details']['payment_method'],
                self.foriegn_ids['user_account_id']
            )
            payment_details = pd_presenter.dict_to_payment_details(
                self.request_json['payment_details']
            )
            if pd_presenter.payment_detail_is_new:
                db.session.add(payment_details)

            # Add notifictions
            db.session.bulk_save_objects([Notification(
                notification_days,
                new_tenancy.id
            ) for notification_days in self.request_json['notifications']])

            # Add tenant_bills and tenant_bill_histories
            rent_schedule_selector = RentSchedulerSelector(new_tenancy)
            tenant_bills = rent_schedule_selector.get_tenant_bills()
            db.session.bulk_save_objects(tenant_bills, return_defaults=True)
            tenant_bill_histories = [
                TenantBillHistory(tenant_bill) for tenant_bill in tenant_bills
            ]
            db.session.bulk_save_objects(tenant_bill_histories)
            
            db.session.commit()
            self.response = jsonify({
                'status': 'success',
                'data': { 'tenancy': [{ 'id': new_tenancy.id }] }
            }), 201
        except Exception as ex:
            print(traceback.format_exc())
            self.response = jsonify({'status': 'fail'}), 400
            db.session.rollback()
        finally:
            return self.response


class SaveTenancyNotesAPI(MethodView):
    ''' Save Tenancy Notes '''
    def post(self):
        ''' Process '''
        return jsonify({'status': 'fail'}), 400


class SaveTenancyEndDateAPI(MethodView):
    ''' Save Tenancy End Date '''
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


# Define the API resources
list_tenancies_view = ListTenanciesAPI.as_view('list_property')
add_new_tenancy_view = AddNewTenancyAPI.as_view('add_property')
get_tenancy_view = GetTenancyAPI.as_view('get_property')
save_tenancy_notes_view = SaveTenancyNotesAPI.as_view('save_tenancy_notes')
save_tenancy_enddate_view = SaveTenancyEndDateAPI.as_view(
    'save_tenancy_enddate'
)
delete_tenancy_view = DeleteTenancyAPI.as_view('delete_property')

# Add rules for API Endpoints
tenancy_blueprint.add_url_rule(
    '/tenancy/list',
    view_func=list_tenancies_view,
    methods=['GET']
)
tenancy_blueprint.add_url_rule(
    '/tenancy/addnew',
    view_func=add_new_tenancy_view,
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
