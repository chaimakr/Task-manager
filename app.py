import datetime
from functools import wraps
from ssl import create_default_context
from flask import Flask, render_template, session, url_for , request , redirect , flash
from flask_sqlalchemy import SQLAlchemy
from database import create_db
from flask_session import Session
import requests


app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
sess = Session(app)

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


@app.route('/', methods=['GET'])
def index():
    if session['logged_in'] == True:
        return render_template('index.html', tasks = Todo.query.filter_by(owner_id = session['iduser']).all())
    else:    
        return render_template('home.html')



@app.route("/login", methods=['GET'])
def login_get():
    if('username' in session):
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route("/login",methods=['POST'])
def login_post():
    user = User.query.filter_by(username=request.form['username']).first()
    if user is None:
        return redirect(url_for('login_get'))
    if user.password == request.form['password']:
        session['logged_in'] = True
        session['username'] = user.username
        session['iduser'] = user.id
        return redirect(url_for('tasks', session=session))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    if session['logged_in'] == True:
        session['logged_in'] = False
        session.pop('username')
        session.pop('iduser')
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))



@app.route("/signup", methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username= request.form['username']
        password= request.form['password']
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue signing up'
    else:
        flash('User already exists')
        return render_template('signup.html')


    

@app.route('/tasks', methods=['GET'])
def tasks():
    tasks = Todo.query.filter_by(owner_id = session['iduser']).all()
    return render_template('index.html', tasks=tasks)


@app.route('/add/<int:iduser>', methods=['POST'])
def add_task(iduser):
    task_content= request.form['content']
    new_task = Todo(content=task_content,owner_id=iduser)

    try:
        db.session.add(new_task)
        db.session.commit()
        return redirect('/')
    except:
        return 'there was an issue adding your task'  



@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)



@app.route('/delete/<int:iduser>/<int:id>')
def detele_task(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/done/<int:id>')
def update_task_state(id):
    task = Todo.query.get_or_404(id)
    if task.state == 0:
        task.state = 1
    else:  
        task.state = 0 
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue changing the state of your task'


def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))    
if __name__ == '__main__':
    app.secret_key = 'strawhatt4'
    app.config['SESSION_TYPE'] = 'filesystem' 
    sess.init_app(app)
    app.run(debug=True)
