'''
All API endpoints that handle tenancy entities and actions
'''

# import traceback
from datetime import datetime
from flask.views import MethodView
from flask import Blueprint, request, jsonify, session
from sqlalchemy import and_, func

from project.server import db, app
from project.server.models.auth import User
from project.server.models.tenancy import Tenancy, TenancyHistory
from project.server.models.tenant import Tenant
from project.server.models.notifications import Notification
from project.server.models.tenant_bill import (RentSchedulerSelector,
                                               TenantBill,
                                               TenantBillHistory,
                                               TenantBillStatus)
from project.server.models.type_values import (RentType, PaymentTerms,
                                               TenancyStatus)


UNKNOWN_ITEM_TYPE = 'Payment type or Rent type unknown'


tenancy_blueprint = Blueprint('tenancy', __name__)


class ListTenanciesAPI(MethodView):
    ''' Return list of tenancies belonging to user '''
    def get(self):
        '''
        Get tenacies belonging to user's account and associated information
        '''
        try:
            # Get query to get tenant names
            tenant_names_query = db.session.query(
                Tenant.tenancy_id,
                func.group_concat(Tenant.name).label('tenant_names')
            ).group_by(Tenant.tenancy_id).subquery()
            # Get query to get tenant bills
            next_payment_query = db.session.query(
                TenantBill.id
            ).outerjoin(
                TenantBillStatus,
                TenantBill.tenant_bill_status_id == TenantBillStatus.id
            ).filter(and_(
                TenantBill.tenancy_id == Tenancy.id,
                TenantBillStatus.value == 'unpaid'
            )).order_by(
                TenantBill.due_date.asc()
            ).limit(1).correlate(Tenancy).subquery()
            # Get tenancy display rows
            tenancy_rows = db.session.query(
                Tenancy,
                tenant_names_query.c.tenant_names,
                PaymentTerms.value,
                RentType.value,
                TenantBill.due_date,
                TenancyStatus.value
            ).outerjoin(
                User,
                User.account_id == Tenancy.account_id
            ).outerjoin(
                tenant_names_query,
                Tenancy.id == tenant_names_query.c.tenancy_id
            ).outerjoin(
                PaymentTerms,
                Tenancy.payment_terms_id == PaymentTerms.id
            ).outerjoin(
                RentType,
                Tenancy.rent_type_id == RentType.id
            ).outerjoin(
                TenantBill,
                next_payment_query == TenantBill.id
            ).outerjoin(
                TenancyStatus,
                Tenancy.tenancy_status_id == TenancyStatus.id
            ).filter(and_(User.id == int(session.pop('user_id', None)),
                          Tenancy.is_deleted == False)).all()
            response = jsonify({
                'status': 'success',
                'd': {'tenancy_list': [{
                    'Tenancy': row.Tenancy,
                    'TenantsNames': row[1],
                    'PaymentTerms': row[2],
                    'RentType': row[3],
                    'NextPayment': row[4],
                    'TenancyStatus': row[5]
                } for row in tenancy_rows]}
            }), 200
        except Exception as ex:
            response = jsonify({'status': 'fail'}), 400
            db.session.rollback()
        finally:
            return response


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
            request_json = request.get_json()
            # Get required foriegn keys. If not successful, throw error
            foreign_ids_set = db.session.query(
                User.account_id,
                RentType.id,
                PaymentTerms.id
            ).filter(
                User.id == int(session.pop('user_id', None))
            ).filter(
                RentType.value == request_json['tenancy']['rent_type']
            ).filter(
                PaymentTerms.value == request_json['tenancy'][
                    'payment_terms'
                ]
            ).first()
            if foreign_ids_set == None or None in foreign_ids_set:
                response = jsonify({
                    'status': 'fail',
                    'message': UNKNOWN_ITEM_TYPE
                }), 400
            foriegn_ids = {
                'user_account_id': foreign_ids_set[0],
                'rent_type_id': foreign_ids_set[1],
                'payment_terms_id': foreign_ids_set[2]
            }
            # Tenancy cannot have zero tenants or notifications
            if not request_json['tenants'] or not request_json['notifications']:
                raise Exception('Tenants or notifications cannot be zero.')
            # Add Tenancy and TenancyHistory to database
            new_tenancy = Tenancy()
            new_tenancy.set_tenancy_dates(
                datetime.strptime(request_json['tenancy']['start_date'],
                                  app.config['DATE_FMT']),
                datetime.strptime(request_json['tenancy']['end_date'],
                                  app.config['DATE_FMT'])
            )
            new_tenancy.address = request_json['tenancy']['address']
            new_tenancy.rent_type_id = foriegn_ids['rent_type_id']
            if request_json['tenancy']['rent_type'] == 'Private Rooms':
                new_tenancy.room_name = request_json['tenancy'][
                    'room_name'
                ]
            new_tenancy.set_rent_cost(
                round(float(request_json['tenancy']['rent_cost']), 2),
                foriegn_ids['payment_terms_id']
            )
            new_tenancy.payment_description = request_json['tenancy'][
                'payment_description'
            ]
            new_tenancy.account_id = foriegn_ids['user_account_id']
            db.session.add(new_tenancy)
            db.session.flush()
            db.session.add(TenancyHistory(updated_tenancy=new_tenancy))

            # Add Tenants to database
            db.session.bulk_save_objects([Tenant(
                tenant_name,
                new_tenancy.id
            ) for tenant_name in request_json['tenants']])

            # Add notifictions
            db.session.bulk_save_objects([Notification(
                notification_days,
                new_tenancy.id
            ) for notification_days in request_json['notifications']])
            # Add tenant_bills and tenant_bill_histories
            rent_schedule_selector = RentSchedulerSelector(new_tenancy)
            tenant_bills = rent_schedule_selector.get_tenant_bills()
            db.session.bulk_save_objects(tenant_bills, return_defaults=True)
            tenant_bill_histories = [
                TenantBillHistory(tenant_bill) for tenant_bill in tenant_bills
            ]
            db.session.bulk_save_objects(tenant_bill_histories)
            
            db.session.commit()
            response = jsonify({
                'status': 'success',
                'd': {'tenancy_id': new_tenancy.id}
            }), 201
        except Exception:
            response = jsonify({'status': 'fail'}), 400
            db.session.rollback()
        finally:
            return response


class EditTenancyAPI(MethodView):
    ''' Save Tenancy '''
    def post(self):
        ''' Process '''
        return jsonify({'status': 'fail'}), 400


# Must determine if we need this:
class SaveTenancyNotesAPI(MethodView):
    ''' Save Tenancy Notes '''
    def post(self):
        ''' Process '''
        return jsonify({'status': 'fail'}), 400


# Must determine if we need this:
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
list_tenancies_view = ListTenanciesAPI.as_view('list_tenancy')
add_new_tenancy_view = AddNewTenancyAPI.as_view('add_tenancy')
get_tenancy_view = GetTenancyAPI.as_view('get_tenancy')
edit_tenancy_view = EditTenancyAPI.as_view('edit_tenancy')
save_tenancy_notes_view = SaveTenancyNotesAPI.as_view('save_tenancy_notes')
save_tenancy_enddate_view = SaveTenancyEndDateAPI.as_view(
    'save_tenancy_enddate'
)
delete_tenancy_view = DeleteTenancyAPI.as_view('delete_tenancy')


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
    '/tenancy/edit',
    view_func=edit_tenancy_view,
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
