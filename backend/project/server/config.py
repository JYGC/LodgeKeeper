'''
project/server/config.py
'''

import os
basedir = os.path.abspath(os.path.dirname(__file__))
postgres_local_base = 'mysql://lodgekeeper:Test3r$@localhost/'
database_name = 'lodgekeeper'


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AUTH_DURATION = 24 * 60 * 60
    EXCLUDE_FROM_AUTHENTICATION = [
        '/auth/register',
        '/auth/login'
    ]
    DATE_FMT = '%Y-%m-%d'
    LETTER_DATE_FMT = '%d %b %Y'


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = postgres_local_base + database_name + '_test'
    AUTH_DURATION = 5
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = 'my_precious'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql:///example'
