import decimal
from datetime import datetime
from flask import Blueprint, request, make_response, jsonify, session
from flask.views import MethodView
from sqlalchemy import and_

from project.server.models.property import Property, PropertyType, RentType
from project.server.models.auth import User
from project.server import db
from project.server.error_handling.exceptions import ItemTypeError

ITEM_NOT_EXISTS_MSG = 'Property not found'
UNKNOWN_ITEM_TYPE = 'Porperty type or Rent type unknown'

property_blueprint = Blueprint('property', __name__)

class PropertyAPI(MethodView):
    '''Return property list'''
    def get(self):
        try:
            user_id = int(session.pop('user_id', None))
            property_list = db.session.query(
                Property,
                PropertyType,
                RentType
            ).outerjoin(
                User,
                Property.account_id == User.account_id
            ).outerjoin(
                PropertyType,
                Property.property_type_id == PropertyType.id
            ).outerjoin(
                RentType,
                Property.rent_type_id == RentType.id
            ).filter(and_(
                User.id == user_id,
                Property.is_deleted == False
            )).all()

            return jsonify({
                'status': 'success',
                'data': {
                    'property': [{
                        'id': row.Property.id,
                        'address': row.Property.address,
                        'property_type': row.PropertyType.value,
                        'rent_type': row.RentType.value,
                        'description': row.Property.description,
                        'parking': row.Property.parking,
                        'rent_cost': round(float(row.Property.rent_cost), 2),
                        'date_constructed': row.Property.date_constructed
                    } for row in property_list]
                }
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'fail',
                'message': 'Failed to get data'
            }), 403


class ManageOnePropertyAPI(MethodView):
    return_res = None

    def get_foriegn_ids(self):
        # Get user, rent and property id all once to reduce database
        # requests
        foriegn_ids_set = db.session.query(
            User.account_id,
            PropertyType.id,
            RentType.id
        ).filter(
            User.id == int(session.pop('user_id', None))
        ).filter(
            PropertyType.value == self.post_data.get('property_type')
        ).filter(
            RentType.value == self.post_data.get('rent_type')
        ).first()

        if foriegn_ids_set == None:
            self.return_res = jsonify({
                'status': 'fail',
                'message': UNKNOWN_ITEM_TYPE
            }), 400
            raise ItemTypeError(UNKNOWN_ITEM_TYPE)

        self.foriegn_ids = {
            'user_account_id': foriegn_ids_set[0],
            'property_type_id': foriegn_ids_set[1],
            'rent_type_id': foriegn_ids_set[2]
        }

    def get_cur_property(self):
        raise NotImplementedError()

    def update_property(self):
        raise NotImplementedError()

    def success_result(self):
        raise NotImplementedError()
    
    def fail_result(self, ex):
        self.return_res = jsonify({
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }), 403

    def post(self):
        self.post_data = request.get_json()
        try:
            self.get_foriegn_ids()            
            self.get_cur_property()
            self.update_property()
            db.session.commit()

            self.success_result()
        except Exception as ex:
            if self.return_res == None:
                self.fail_result(ex)

        return self.return_res


class PropertyAddAPI(ManageOnePropertyAPI):
    def get_cur_property(self):
        new_property = Property()
        new_property.address = self.post_data.get('address')
        new_property.property_type_id = self.foriegn_ids['property_type_id']
        new_property.rent_type_id = self.foriegn_ids['rent_type_id']
        new_property.description = None if len(self.post_data.get(
            'description'
        ).strip()) == 0 else self.post_data.get('description')
        new_property.parking = self.post_data.get('parking')
        new_property.rent_cost = float(self.post_data.get('rent_cost'))
        new_property.date_constructed = datetime.strptime(
            self.post_data.get('date_constructed'),
            '%Y-%m-%d'
        )
        new_property.account_id = self.foriegn_ids['user_account_id']
        self.cur_property = new_property

    def update_property(self):
        db.session.add(self.cur_property)
        # Get new propety id to return to client side
        db.session.flush()

    def success_result(self):
        self.return_res = jsonify({
            'status': 'success',
            'data': {
                'property': [{ 'id': self.cur_property.id }]
            }
        }), 201


class PropertyEditAPI(ManageOnePropertyAPI):
    def get_cur_property(self):
        self.cur_property = db.session.query(Property).filter(and_(           
            Property.id == int(self.post_data.get('id')),
            Property.account_id == self.foriegn_ids['user_account_id']
        )).first()

        if self.cur_property is None:
            self.return_res = jsonify({
                'status': 'fail',
                'message': ITEM_NOT_EXISTS_MSG
            }), 400
            raise ValueError(ITEM_NOT_EXISTS_MSG)

    def update_property(self):
        self.cur_property.address = self.post_data.get('address')
        self.cur_property.property_type_id = self.foriegn_ids[
            'property_type_id'
        ]
        self.cur_property.rent_type_id = self.foriegn_ids[
            'rent_type_id'
        ]
        self.cur_property.description = self.post_data.get(
            'description'
        )
        self.cur_property.parking = bool(self.post_data.get('parking'))
        self.cur_property.rent_cost = round(float(
            self.post_data.get('rent_cost')
        ), 2)
        self.cur_property.date_constructed = datetime.strptime(
            self.post_data.get('date_constructed'),
            '%Y-%m-%d'
        )

    def success_result(self):
        self.return_res = jsonify({ 'status': 'success' }), 200


class PropertyGetAPI(MethodView):
    def post(self):
        self.post_data = request.get_json()
        try:
            self.cur_property = db.session.query(
                Property,
                PropertyType,
                RentType
            ).outerjoin(
                PropertyType,
                Property.property_type_id == PropertyType.id
            ).outerjoin(
                RentType,
                Property.rent_type_id == RentType.id
            ).outerjoin(
                User,
                Property.account_id == User.account_id
            ).filter(and_(
                Property.id == int(self.post_data.get('id')),
                User.id == int(session.pop('user_id', None))
            )).first()
            if self.cur_property is None:
                return jsonify({
                    'status': 'fail',
                    'message': ITEM_NOT_EXISTS_MSG
                }), 400
            return jsonify({
                'status': 'success',
                'data': {
                    'property' :  [{
                        'id': self.cur_property.Property.id,
                        'address': self.cur_property.Property.address,
                        'property_type': (
                            self.cur_property.PropertyType.value
                        ),
                        'rent_type': self.cur_property.RentType.value,
                        'description': self.cur_property.Property.description,
                        'parking': self.cur_property.Property.parking,
                        'rent_cost': round(float(
                            self.cur_property.Property.rent_cost
                        ), 2)
                    }]
                }
            }), 200
        except Exception as ex:
            print(ex)
        return jsonify({ 'status': 'fail' }), 401


class PropertyDeleteAPI(MethodView):
    def post(self):
        self.post_data = request.get_json()
        try:
            self.cur_property = db.session.query(Property).outerjoin(
                User,
                Property.account_id == User.account_id
            ).filter(and_(
                Property.id == int(self.post_data.get('id')),
                User.id == int(session.pop('user_id', None))
            )).first()
            if self.cur_property is None:
                return jsonify({
                    'status': 'fail',
                    'message': ITEM_NOT_EXISTS_MSG
                }), 400
            self.cur_property.is_deleted = True
            return jsonify({ 'status': 'success' }), 200
        except:
            pass

        return jsonify({ 'status': 'fail' }), 401


# define the API resources
property_view = PropertyAPI.as_view('property')
property_add_view = PropertyAddAPI.as_view('property_add')
property_edit_view = PropertyEditAPI.as_view('property_edit')
property_get_view = PropertyGetAPI.as_view('property_get')
property_delete_view = PropertyDeleteAPI.as_view('property_delete')

# add Rules for API Endpoints
property_blueprint.add_url_rule(
    '/property',
    view_func=property_view,
    methods=['GET']
)
property_blueprint.add_url_rule(
    '/property/add',
    view_func=property_add_view,
    methods=['POST']
)
property_blueprint.add_url_rule(
    '/property/edit',
    view_func=property_edit_view,
    methods=['POST']
)
property_blueprint.add_url_rule(
    '/property/get',
    view_func=property_get_view,
    methods=['POST']
)
property_blueprint.add_url_rule(
    '/property/delete',
    view_func=property_delete_view,
    methods=['POST']
)
