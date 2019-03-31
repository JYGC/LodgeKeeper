"""
property/server/models/property.py
"""

from project.server import db

class Property(db.Model):
    """ Property Model for storing property data """
    __tablename__ = "property"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address = db.Column(db.String(255), nullable=False)
    #property_type = db.Column(db.Integer, db.ForeignKey('property_type.id'),
    #                          nullable=False)
    #rent_type = db.Column(db.Integer, db.ForeignKey('rent_type.id'),
    #                      nullable=False)
    description = db.Column(db.String(10000))
    parking = db.Column(db.Boolean, nullable=False)
    rent_cost = db.Column(db.Numeric(12, 2))
    is_deleted = db.Column(db.Boolean)
    date_constructed = db.Column(db.DateTime, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    #account_id = db.Column(db.Integer, db.ForeignKey('account.id'),
    #                       nullable=False)

    def __init__(self, address, description, parking, rent_cost, is_delete,
                 date_constructed, date_created):
        self.address = address
        self.description = description
        self.parking = parking
        self.rent_cost = rent_cost
        self.is_deleted = is_delete
        self.date_constructed = date_constructed
        self.date_created = date_created

#class 
