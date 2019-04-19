from project.tests.base import BaseTestCase

from project.tests import actions
from project.tests import values

class TestAddTenancyAPI(BaseTestCase):
    ''' Test views in Property Blueprint '''
    def setup_actions(self):
        ''' Initialize Action objects '''
        self.register_user = actions.user.RegisterUser(self)
    
    def test_add_tenancy(self):
        ''' Test adding new tenancy '''
        with self.client:
            user_data = self.register_user.run(
                values.auth_values.test_user_values
            )
    
    def test_add_tenancy_with_invalid_token(self):
        ''' Test adding new tenancy with invalid token '''
    
    def test_add_tenancy_with_foriegn_table_values(self):
        ''' Test adding new tenancy with foriegn table values '''
