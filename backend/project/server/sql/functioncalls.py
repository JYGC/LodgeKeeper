from project.server import db


class FunctionCall():
    _select_statement = 'SELECT * FROM %s'
    _name = 'func_name(:func_params)'

    def call(self, **args):
        sqlcall = db.session.execute(self._select_statement % self._name,
                                        args)
        return sqlcall.fetchall()
    

class SpListTenancies(FunctionCall):
    _name = 'sp_list_tenancies(:user_id)'


class FnAllNextPaymentDueDates(FunctionCall):
    _name = 'fn_all_next_payment_duedates(:user_id)'


class FnTenantNamesArray(FunctionCall):
    _name = 'fn_tenant_names_array(:user_id)'
