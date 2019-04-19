from project.server import db


class IValueModel():
    type_values = {}

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), nullable=False)

    def __init__(self, id, value):
        self.id = id
        self.value = value

    @classmethod
    def update_type_data(self: db.Model):
        type_list = self.query.all()
        type_dict = dict(zip([cur_type.id for cur_type in type_list], 
                             type_list))
        for key, value in self.type_values.items():
            if key in type_dict:
                # If type exists just update value
                type_dict[key].value = value
            else:
                db.session.add(self(key, value))
            
            if key in type_dict:
                type_dict.pop(key)
        for id in type_dict.keys():
            # delete values that are not in type_values
            self.query.filter(self.id == id).delete()
        db.session.commit()


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
    type_values = { 1: 'Monthly', 2: 'Fortnightly', 3: 'Lump sum' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class PaymentMethod(db.Model, IValueModel):
    ''' Model to manage payment methods '''
    __tablename__ = 'payment_method'
    type_values = { 1: 'Bank Transfer', 2: 'PayPal', 3: 'Cash' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class TenancyStatus(db.Model, IValueModel):
    ''' Model to manage tenancy status '''
    __tablename__ = 'tenancy_status'
    type_values = { 1: 'Active', 2: 'Ended', 3: 'Terminated', 4: 'Abandoned',
                    5: 'Suspended' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class TenantBillType(db.Model, IValueModel):
    ''' Model to manage tenanc bill type '''
    __tablename__ = 'tenant_bill_type'
    type_values = { 1: 'other', 2: 'rent' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)


class TenantBillStatus(db.Model, IValueModel):
    ''' Model to manage tenant bill status '''
    __tablename__ = 'tenant_bill_status'
    type_values = { 1: 'other', 2: 'rent' }

    def __init__(self, id, value):
        super().__init__(id=id, value=value)
