# project/tests/base.py


from flask_testing import TestCase

from project.server import app, db, models


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        models.type_values.InitializeTypeValue.update_default_data()
        db.session.commit()
        self.setup_actions()

    def setup_actions(self):
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()
