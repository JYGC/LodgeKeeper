'''
Type Value models and interfaces
'''

from typing import List

from project.server import db


class IValueModel():
    type_values = {}

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)

    def __init__(self, id, value):
        self.id = id
        self.value = value


class IValueModelSelectableIds(IValueModel):
    @classmethod
    def get_value_id(self, value):
        return dict(zip(self.type_values.values(), self.type_values.keys()))[
            value
        ]


class PropertyType(db.Model, IValueModel):
    ''' Model to manage property types '''
    __tablename__ = 'property_type'
    type_values = { 1: 'Landed House', 2: 'Apartment' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class RentType(db.Model, IValueModel):
    ''' Model to manage rent type '''
    __tablename__ = 'rent_type'
    type_values = { 1: 'Whole Property', 2: 'Private Rooms' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class PaymentTerms(db.Model, IValueModel):
    ''' Model to manage payment type '''
    __tablename__ = 'payment_terms'
    type_values = { 1: 'Per week', 2: 'Per fortnight', 3: 'Per month' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class PaymentMethod(db.Model, IValueModel):
    ''' Model to manage payment methods '''
    __tablename__ = 'payment_method'
    type_values = { 1: 'Cash', 2: 'PayPal', 3: 'Bank Transfer' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class TenantBillType(db.Model, IValueModelSelectableIds):
    ''' Model to manage tenanc bill type '''
    __tablename__ = 'tenant_bill_type'
    type_values = { 1: 'other', 2: 'rent' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class TenantBillStatus(db.Model, IValueModelSelectableIds):
    ''' Model to manage tenant bill status '''
    __tablename__ = 'tenant_bill_status'
    type_values = { 1: 'unpaid', 2: 'paid', 3: 'waivered' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)

class InitializeTypeValue():
    @staticmethod
    def update_default_data():
        value_model_list: List[IValueModel] = [
            PaymentMethod,
            PaymentTerms,
            PropertyType,
            RentType,
            TenantBillStatus,
            TenantBillType
        ]
        for value_model in value_model_list:
            type_list = value_model.query.all()
            type_dict = dict(zip([cur_type.id for cur_type in type_list], 
                                type_list))
            for key, value in value_model.type_values.items():
                if key in type_dict:
                    # If type exists just update value
                    type_dict[key].value = value
                else:
                    db.session.add(value_model(key, value))
                
                if key in type_dict:
                    type_dict.pop(key)
            for id in type_dict.keys():
                # delete values that are not in type_values
                value_model.query.filter(value_model.id == id).delete()
            db.session.commit()
