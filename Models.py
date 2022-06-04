
import datetime
from . import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def __repr__(self):
    return '<Task %r>' % self.id