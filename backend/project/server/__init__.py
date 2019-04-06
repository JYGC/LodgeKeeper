# project/server/__init__.py

import os

from flask import Flask, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.server.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.server.helpers.auth import AuthTokenValidator
token_validator = AuthTokenValidator()
app.before_request(token_validator.validate)

from project.server.controllers.auth import auth_blueprint
app.register_blueprint(auth_blueprint)
from project.server.controllers.property import property_blueprint
app.register_blueprint(property_blueprint)
