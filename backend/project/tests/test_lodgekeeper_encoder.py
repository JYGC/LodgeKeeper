'''
project/tests/test_lodgekeeper_encoder.py
'''


from datetime import datetime
from decimal import Decimal
import unittest

from project.tests.base import BaseTestCase
from project.tests.values import tenancy_values
from project.server.type_helpers.json import LodgeKeeperEncoder
from project.server import app
from project.server.models.tenancy import Tenancy


class TestLodgeKeeperEncoder(BaseTestCase):
    '''
    Test JSONEncoder modified to encode db.Models, decimals, and datetime
    '''

    def test_encode_decimal(self):
        ''' Test encoding decimals to JSON '''
        obj = Decimal(7.54)
        encoder = LodgeKeeperEncoder()
        json_compatible = encoder.default(obj)
        self.assertIsInstance(json_compatible, float)
        self.assertEqual(Decimal(json_compatible), obj)
    
    def test_encode_datetime(self):
        ''' Test encoding datetime to JSON '''
        obj = datetime(2020, 10, 4)
        encoder = LodgeKeeperEncoder()
        json_compatible = encoder.default(obj)
        self.assertIsInstance(json_compatible, str)
        self.assertEqual(json_compatible, obj.strftime(app.config['DATE_FMT']))

    def test_encode_tenancy_model(self):
        ''' Test encoding models to JSON '''
        obj = Tenancy()
        obj.start_date = tenancy_values.NEW_PRIVATE_ROOM['start_date']
        obj.end_date = tenancy_values.NEW_PRIVATE_ROOM['end_date']
        obj.address = tenancy_values.NEW_PRIVATE_ROOM['address']
        obj.room_name = tenancy_values.NEW_PRIVATE_ROOM['room_name']
        obj.rent_cost = tenancy_values.NEW_PRIVATE_ROOM['rent_cost']
        encoder = LodgeKeeperEncoder()
        json_compatible = encoder.default(obj)
        self.assertIsInstance(json_compatible, dict)
        self.assertEqual(obj.start_date, json_compatible['start_date'])
        self.assertEqual(obj.end_date, json_compatible['end_date'])
        self.assertEqual(obj.address, json_compatible['address'])
        self.assertEqual(obj.room_name, json_compatible['room_name'])
        self.assertEqual(obj.rent_cost, json_compatible['rent_cost'])
        self.assertEqual(obj.rent_cost_per_week, json_compatible[
            'rent_cost_per_week'
        ])
    

if __name__ == '__main__':
    unittest.main()
