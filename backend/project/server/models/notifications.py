from project.server import db


class Notification(db.Model):
    ''' Model to manage notification data '''
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    days = db.Column(db.Integer, nullable=False)
    tenancy_id = db.Column(db.Integer, db.ForeignKey('tenancy.id'),
                           nullable=False)
