'''
Tenancy API endpoint test cases
'''

import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.actions.user import RegisterUser, RegisterUserApiAction
from project.tests.actions.list_tenancy import (
    ListTenancyApiAction,
    ChkListTenancyResponseAction
)
from project.tests.actions.add_new_tenancy import (
    AddTenancyApiAction,
    ChkAddTenancyResponseAction,
    ChkAddTenancyDbStateAction
)
from project.tests.actions.failed_response import (
    ChkResponseActionBadRequest,
    ChkResponseActionInvaildToken
)
from project.tests import values


def register_user_get_auth_token(test_cls):
    return json.loads(RegisterUserApiAction.run(
        test_cls,
        values.auth_values.test_user_values['user_1']
    ).data.decode())['auth_token']


class TestListTenancies(BaseTestCase):
    ''' Test list Tenancy endpoint '''

    def test_list_no_tenancies(self):
        ''' Test listing tenancies with no tenancies '''
        with self.client:
            ChkListTenancyResponseAction.run(
                self,
                dict(),
                ListTenancyApiAction.run(
                    self,
                    register_user_get_auth_token(self)
                )
            )

    def test_list_one_tenancy(self):
        ''' Test listing tenancies with one tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            tenancy_id = json.loads(AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['tenancy_list'][
                    2
                ],
                auth_token
            ).data.decode())['d']['tenancy_id']
            ChkListTenancyResponseAction.run(self, {
                tenancy_id: values.tenancy_values.test_new_tenancy_values[
                    'tenancy_list'
                ][2]
            }, ListTenancyApiAction.run(self, auth_token))

    def test_list_ten_tenancies(self):
        ''' Test listing tenancies with ten tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            test_tenancy_list_dict = dict()
            for test_tenancy in values.tenancy_values.test_new_tenancy_values[
                'tenancy_list'
            ]:
                test_tenancy_list_dict[
                    json.loads(AddTenancyApiAction.run(
                        self,
                        test_tenancy,
                        auth_token
                    ).data.decode())['d']['tenancy_id']
                ] = test_tenancy

            ChkListTenancyResponseAction.run(self, test_tenancy_list_dict,
                                             ListTenancyApiAction.run(
                                                 self,
                                                 auth_token
                                             ))


class TestAddTenancyAPI(BaseTestCase):
    ''' Test add tenancy endpoint '''
    
    def test_add_private_room_tenancy(self):
        ''' Test adding a new private room tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['private_room'],
                auth_token
            )
            ChkAddTenancyResponseAction.run(self, resp_addtenancy)
            ChkAddTenancyDbStateAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['private_room'],
                resp_addtenancy
            )
    
    def test_add_whole_property_tenancy(self):
        ''' Tets adding a new whole property tenancy '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['whole_property'],
                auth_token
            )
            ChkAddTenancyResponseAction.run(self, resp_addtenancy)
            ChkAddTenancyDbStateAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['whole_property'],
                resp_addtenancy
            )
    
    def test_add_tenancy_with_invalid_token(self):
        ''' Test adding new tenancy with invalid token '''
        with self.client:
            register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['private_room'],
                '000000000000000000000000'
            )
            ChkResponseActionInvaildToken.run(self, resp_addtenancy)
    
    def test_add_tenancy_with_bad_foriegn_table_values(self):
        ''' Test adding new tenancy with bad foriegn table values '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['with_bad_types'],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)
    
    def test_add_tenancy_no_tenants(self):
        ''' Test adding tenancy without tenants '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values['no_tenants'],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)

    def test_add_tenancy_no_notifications(self):
        ''' Test adding tenancy without notifications '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values[
                    'no_notifications'
                ],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)

    def test_add_tenancy_no_tenants_and_notifications(self):
        ''' Test adding tenancy without tenants and notifications '''
        with self.client:
            auth_token = register_user_get_auth_token(self)
            resp_addtenancy = AddTenancyApiAction.run(
                self,
                values.tenancy_values.test_new_tenancy_values[
                    'no_tenants_and_notifications'
                ],
                auth_token
            )
            ChkResponseActionBadRequest.run(self, resp_addtenancy)

    # def test_add_tenancy_with_cash_details(self):
    #     ''' Test adding new tenancy with cash payment method '''
    #     with self.client:
    #         user_data = self.register_user.run(
    #             values.auth_values.test_user_values['user_1']
    #         )
    #         self.add_new_tenancy_with_cash.run(
    #             user_data['auth_token'],
    #             values.tenancy_values.test_new_tenancy_values['with_cash']
    #         )
    
    # def test_add_tenancy_with_paypal_details(self):
    #     ''' Test adding new tenancy with paypal payment method '''
    #     with self.client:
    #         user_data = self.register_user.run(
    #             values.auth_values.test_user_values['user_1']
    #         )
    #         self.add_new_tenancy_with_paypal.run(
    #             user_data['auth_token'],
    #             values.tenancy_values.test_new_tenancy_values['with_paypal']
    #         )
    
    # def test_add_tenancy_with_bank_details(self):
    #     ''' Test adding new tenancy with bank payment method '''
    #     with self.client:
    #         user_data = self.register_user.run(
    #             values.auth_values.test_user_values['user_1']
    #         )
    #         self.add_new_tenancy_with_bank.run(
    #             user_data['auth_token'],
    #             values.tenancy_values.test_new_tenancy_values[
    #                 'with_bank_transfer'
    #             ]
    #         )

class TestEditTenancyAPI(BaseTestCase):
    ''' Test Edit tenancy endpoint '''
    def test_edit_unstarted_tenancy_changed_address(self):
        ''' Test changing unstarted tenancy property address '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_tenancy_no_address(self):
        ''' Test removing unstarted tenancy property address '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_tenancy_changed_rent_type_to_whole_property(self):
        ''' Test changing unstarted tenancy rent type '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_tenancy_changed_rent_type_to_private_room(self):
        ''' Test changing unstarted tenancy rent type '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_tenancy_no_rent_type(self):
        ''' Test removing unstarted tenancy rent type '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_private_room_tenancy_change_room_name(self):
        '''
        Test changing room name of unstarted tenancy with rent type private room
        '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_private_room_tenancy_no_room_name(self):
        '''
        Test remove room name of unstarted tenancy with rent type private room
        '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_whole_property_tenancy_add_room_name(self):
        '''
        Test adding room name of unstarted tenancy with rent type whole property
        '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_tenancy_change_start_date_to_lt_end_date(self):
        '''
        Test changing start date of unstarted tenancy to less than end date
        '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_tenancy_change_start_date_to_gt_end_date(self):
        '''
        Test changing start date of unstarted tenancy to greater than end date
        '''
        with self.client:
            self.assertTrue(False)

    def test_edit_unstarted_tenancy_no_start_date(self):
        ''' Test removing start date of unstarted tenancy '''
        pass

    def test_edit_unstarted_tenancy_change_end_date_to_gt_start_date(self):
        '''
        Test changing end date of unstarted tenancy to greater than start date
        '''
        pass

    def test_edit_unstarted_tenancy_change_end_date_to_lt_start_date(self):
        pass

    def test_edit_unstarted_tenancy_no_end_date(self):
        pass

    def test_edit_unstarted_tenancy_change_tenancy_notes(self):
        pass

    def test_edit_unstarted_tenancy_no_tenancy_notes(self):
        pass

    def test_edit_unstarted_tenancy_terminate(self):
        pass

    def test_edit_unstarted_tenancy_delete(self):
        pass

    def test_edit_active_tenancy_changed_address(self):
        pass

    def test_edit_active_tenancy_no_address(self):
        pass

    def test_edit_active_tenancy_changed_rent_type_to_whole_property(self):
        pass

    def test_edit_active_tenancy_changed_rent_type_to_private_room(self):
        pass

    def test_edit_active_tenancy_no_rent_type(self):
        pass

    def test_edit_active_private_room_tenancy_change_room_name(self):
        pass

    def test_edit_active_private_room_tenancy_no_room_name(self):
        pass

    def test_edit_active_whole_property_tenancy_add_room_name(self):
        '''
        Test adding room name of active tenancy with rent type whole property
        '''
        with self.client:
            self.assertTrue(False)

    def test_edit_active_tenancy_change_start_date_to_lt_end_date(self):
        pass

    def test_edit_active_tenancy_change_start_date_to_gt_end_date(self):
        pass

    def test_edit_active_tenancy_no_start_date(self):
        pass

    def test_edit_active_tenancy_change_end_date_to_gt_start_date(self):
        pass

    def test_edit_active_tenancy_change_end_date_to_lt_start_date(self):
        pass

    def test_edit_active_tenancy_no_end_date(self):
        pass

    def test_edit_Active_tenancy_change_tenancy_notes(self):
        pass

    def test_edit_active_tenancy_no_tenncy_notes(self):
        pass

    def test_edit_active_terminate(self):
        pass

    def test_edit_active_delete(self):
        pass

    def test_edit_ended_tenancy_changed_address(self):
        pass

    def test_edit_ended_tenancy_no_address(self):
        pass

# These tests cases are controlled by one if statement so currently, we only
# test for one field
    # def test_edit_ended_tenancy_changed_rent_type_to_whole_property(self):
    #     pass

    # def test_edit_ended_tenancy_changed_rent_type_to_private_room(self):
    #     pass

    # def test_edit_ended_tenancy_no_rent_type(self):
    #     pass

    # def test_edit_ended_private_room_tenancy_change_room_name(self):
    #     pass

    # def test_edit_ended_private_room_tenancy_no_room_name(self):
    #     pass

    # def test_edit_ended_whole_property_tenancy_add_room_name(self):
    #     '''
    #     Test adding room name of ended tenancy with rent type whole property
    #     '''
    #     with self.client:
    #         self.assertTrue(False)

# Edit Ended Tenancy change start date
# Edit Ended Tenancy change start date to greater than end date
# Edit Ended Tenancy no start date
# Edit Ended Tenancy change end date
# Edit Ended Tenancy change end date to less than start date
# Edit Ended Tenancy change end date to less than start date
# Edit Ended Tenancy no end date
    def test_edit_ended_tenancy_change_tenancy_notes(self):
        pass

    def test_edit_ended_tenancy_no_tenancy_notes(self):
        pass


if __name__ == '__main__':
    unittest.main()
