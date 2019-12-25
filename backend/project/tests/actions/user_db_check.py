from project.server import db
from project.server.models.auth import Account, User


class ChkUserDbState():
    @classmethod
    def run(self, test_cls, test_values, **filter_values):
        user_query = db.session.query(
            User,
            Account
        ).outerjoin(
            Account,
            Account.id == User.account_id
        )
        user_list = self.filter_query(user_query, **filter_values).all()
        self.test_assersions(test_cls, user_list, test_values, **filter_values)
    
    @staticmethod
    def filter_query(tenancy_table, **filter_values):
        None
    
    @staticmethod
    def test_assersions(test_cls, tenancy_list, test_values, **filter_values):
        None


class ChkOneUserInDb(ChkUserDbState):
    @classmethod
    def run(self, test_cls, test_values):
        super().run(test_cls, test_values, **test_values)
    
    @staticmethod
    def filter_query(user_query, **filter_values):
        return user_query.filter(
            User.email == filter_values['email']
        )
    
    @staticmethod
    def test_assersions(test_cls, user_list, test_values, **filter_values):
        test_cls.assertEqual(len(user_list), 1)
