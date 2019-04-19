from project.server import db


class Tenant(db.Model):
    ''' Model to manage Tenant data '''
    __tablename__ = 'tenant'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    tenancy_id = db.Column(db.Integer, db.ForeignKey('tenancy.id'),
                           nullable=False)