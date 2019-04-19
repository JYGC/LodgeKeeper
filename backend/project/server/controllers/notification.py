from flask.views import MethodView
from flask import Blueprint

from project.server.models.notifications import Notification


notification_blueprint = Blueprint('notification', __name__)


class ListNotificationsAPI(MethodView):
    ''' Return all user's tenant bills '''
    def get(self):
        return False, 400


class AddNotificationAPI(MethodView):
    ''' Add tenant bills '''
    def post(self):
        return False, 400


class SaveNotificationAPI(MethodView):
    ''' Save tenant bills '''
    def post(self):
        return False, 400


class DeleteNotificationAPI(MethodView):
    ''' Delete tenant bills '''
    def post(self):
        return False, 400


# define the API resources
list_notifications_view = ListNotificationsAPI.as_view('list_notifications')
add_notification_view = AddNotificationAPI.as_view('add_notification')
save_notification_view = SaveNotificationAPI.as_view('save_notification')
delete_notification_view = DeleteNotificationAPI.as_view('delete_notification')

# Add Rules for API Endpoints
notification_blueprint.add_url_rule(
    '/notification/list',
    view_func=list_notifications_view,
    methods=['GET']
)
notification_blueprint.add_url_rule(
    '/notification/add',
    view_func=add_notification_view,
    methods=['POST']
)
notification_blueprint.add_url_rule(
    '/notification/save',
    view_func=save_notification_view,
    methods=['POST']
)
notification_blueprint.add_url_rule(
    '/notification/delete',
    view_func=delete_notification_view,
    methods=['POST']
)
