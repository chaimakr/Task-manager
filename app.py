import datetime
from ssl import create_default_context
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app =  Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
@app.route('/')

class todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

def __repr__(self):
    return '<Task %r>' % self.id


def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
