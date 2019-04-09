from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project.server.models.property import Property

property_blueprint = Blueprint('property', __name__)

class PropertyAPI(MethodView):
    def get(self):
        return jsonify({ 'status': 'fail' })

class PropertyAddAPI(MethodView):
    def post(self):
        return jsonify({ 'status': 'fail' })

class PropertyEditAPI(MethodView):
    def post(self):
        return jsonify({ 'status': 'fail' })

class PropertyGetAPI(MethodView):
    def post(self):
        return jsonify({ 'status': 'fail' })

class PropertyDeleteAPI(MethodView):
    def post(self):
        return jsonify({ 'status': 'fail' })

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