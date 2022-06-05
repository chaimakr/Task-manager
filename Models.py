
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    state = db.Column(db.Integer, default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def __repr__(self):
    return '<Task %r>' % self.id

class User(db.Model):
    id =  db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Todo', backref = 'User', cascade = 'all, delete-orphan', lazy = 'dynamic')

def __repr__(self):
    return '<Task %r>' % self.id
