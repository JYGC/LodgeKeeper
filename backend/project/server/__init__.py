'''
__init__ file for server directory.

Contains flask app initiation and configuration code, initiating ORM
instances, and connecting blueprints
'''

import os

from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# Create flask app instance, allow cross origin request and set flask app
# configuration
app = Flask(__name__)
CORS(app)
app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)
# create hashing instance and create DB ORM instance
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
from project.server.sql.sqlcalls import SQLFunctionCalls
dbcalls = SQLFunctionCalls()
# Modify json encoder to encode column attributes of sqlalchemy classes,
# decimals and datetimes
from project.server.type_helpers.json import LodgeKeeperEncoder
app.json_encoder = LodgeKeeperEncoder
# Make request authentication run before precessing each request
from project.server.request_helpers.auth import AuthTokenValidator
app.before_request(AuthTokenValidator.validate)
# Coneect flask blueprints
from project.server.apis.user import user_blueprint
app.register_blueprint(user_blueprint)
from project.server.apis.tenancy import tenancy_blueprint
app.register_blueprint(tenancy_blueprint)
from project.server.apis.tenant_bill import tenant_bill_blueprint
app.register_blueprint(tenant_bill_blueprint)
from project.server.apis.notification import notification_blueprint
app.register_blueprint(notification_blueprint)
