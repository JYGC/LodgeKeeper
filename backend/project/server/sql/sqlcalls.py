from sqlalchemy.sql import text
from project.server import db
import os

class InitializeSQL():
    '''
    Helper class containing methods to initialize functions and procedures in
    the database
    '''
    @classmethod
    def update_functions(self):
        self.__update_sql('functions')

    @classmethod
    def update_procedures(self):
        self.__update_sql('procedures')

    @staticmethod
    def __update_sql(query_dirname):
        sql_dirpath = os.path.dirname(os.path.realpath(__file__))
        query_dirpath = os.path.join(sql_dirpath, query_dirname)
        for script in os.listdir(query_dirpath):
            if script.endswith('.sql'):
                scriptpath = os.path.join(query_dirpath, script)
                with open(scriptpath, 'r') as f:
                    sqltext = text(f.read())
                    db.session.execute(sqltext)
        db.session.commit()


from .functioncalls import (SpListTenancies, FnAllNextPaymentDueDates,
                            FnTenantNamesArray)

class SQLFunctionCalls():
    sp_list_tenancies = SpListTenancies()
    fn_all_next_payment_duedates = FnAllNextPaymentDueDates()
    fn_tenant_names_array = FnTenantNamesArray()
