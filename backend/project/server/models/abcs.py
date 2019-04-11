from project.server import db


class TypeModel():
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
