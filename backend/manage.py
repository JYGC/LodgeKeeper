'''
manage.py
'''


import os
import unittest
import coverage

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

from project.server import app, db, models
from project.server.sql import sqlcalls

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    ''' Runs the unit tests without test coverage. '''
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    ''' Runs the unit tests with coverage. '''
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@manager.command
def create_db():
    ''' Creates the db tables. '''
    db.create_all()


@manager.command
def drop_db():
    ''' Drops the db tables. '''
    db.drop_all()


@manager.command
def fill_default_data():
    ''' Update all default data '''
    models.type_values.InitializeTypeValue.update_default_data()


@manager.command
def create_sql():
    ''' Update all functions and stored procedures '''
    sqlcalls.InitializeSQL.update_functions()
    sqlcalls.InitializeSQL.update_procedures()


if __name__ == '__main__':
    manager.run()
