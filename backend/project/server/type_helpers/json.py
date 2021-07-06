import decimal
from flask import json
from datetime import datetime

from project.server import app, db

class LodgeKeeperEncoder(json.JSONEncoder):
    ''' Child class to modify flask JSONEncoder to habdle extra classes '''
    def default(self, obj):
        encoded_obj = None
        if isinstance(obj, db.Model):
            # if obj is SQLAlchemy class
            encoded_obj = {}
            for field in [
                x for x in dir(obj) if not x.startswith('_') and x != 'metadata'
            ]:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # will fail on non-encodable values
                    encoded_obj[field] = data
                except TypeError:
                    pass
        elif isinstance(obj, decimal.Decimal):
            encoded_obj = float(obj)
        elif isinstance(obj, datetime):
            encoded_obj = obj.strftime(app.config['DATE_FMT'])
        else:
            encoded_obj = super(LodgeKeeperEncoder, self).default(obj)
        return encoded_obj
