"""
property/server/models/property.py
"""

import datetime

from project.server import db
from project.server.models.abcs import TypeModel


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
    rent_cost = db.Column(db.Numeric(12, 2))
    is_deleted = db.Column(db.Boolean)
    date_constructed = db.Column(db.DateTime, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                           nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    def __init__(self, address, property_type_id, rent_type_id, description,
                 parking, rent_cost, is_delete, date_constructed, account_id):
        self.address = address
        self.property_type_id = property_type_id
        self.rent_type_id = rent_type_id
        self.description = description
        self.parking = parking
        self.rent_cost = rent_cost
        self.is_deleted = is_delete
        self.date_constructed = date_constructed
        self.account_id = account_id
        self.date_created = datetime.datetime.now()


class PropertyType(db.Model, TypeModel):
    """ Different property types: Landed House or Apartment """
    __tablename__ = 'property_type'
    type_values = {1: 'Landed House', 2: 'Apartment'}

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class RentType(db.Model, TypeModel):
    """ Different rent type: Whole Property or Private Rooms """
    __tablename__ = 'rent_type'
    type_values = {1: 'Whole Property', 2: 'Private Rooms'}

    def __init__(self, id, value):
        super().__init__(id=id, value=value)
