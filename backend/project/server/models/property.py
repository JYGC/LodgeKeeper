"""
property/server/models/property.py
"""

import datetime

from project.server import db


class Property(db.Model):
    """ Property Model for storing property data """
    __tablename__ = 'property'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(255), nullable=False)
    property_type_id = db.Column(db.Integer, db.ForeignKey('property_type.id'),
                                 nullable=False)
    rent_type_id = db.Column(db.Integer, db.ForeignKey('rent_type.id'),
                             nullable=False)
    description = db.Column(db.Text)
    parking = db.Column(db.Boolean, nullable=False)
    rent_cost = db.Column(db.Numeric(12, 2), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False)
    date_constructed = db.Column(db.DateTime, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.date_created = datetime.datetime.now()
        self.is_deleted = False
