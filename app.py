from ast import dump
from flask import Flask, render_template, session, url_for , request , redirect , flash
from flask_session import Session
from Models import db, Todo, User
from database import create_db


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    db.init_app(app)
    return app





@app.route('/', methods=['GET'])
def index():
    if 'logged_in' in session and session['logged_in']:
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
        #print(session)
        session['logged_in'] = True
        session['username'] = user.username
        session['iduser'] = user.id
        return redirect(url_for('get_tasks', session=session))
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    if 'logged_in' in session and session['logged_in']:
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
        try:
            add_user(username,password)
            return redirect('/')
        except:
            return 'there was an issue signing up'
    else:
        return render_template('signup.html')


    

@app.route('/tasks', methods=['GET'])
def get_tasks():
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
    task = Todo.query.filter_by(owner_id = session['iduser'], id = id).first()
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task)



@app.route('/delete/<int:id>')
def detele_task(id):
    task_to_delete = Todo.query.filter_by(owner_id = session['iduser'], id = id).first()

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/done/<int:id>')
def update_task_state(id):
    task = Todo.query.filter_by(owner_id = session['iduser'], id = id ).first()
    if task.state == 0:
        task.state = 1
    else:  
        task.state = 0 
    try:
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue changing the state of your task'
def launch( db='info.db', create=False):
    if create:
        create_db(db)
    os.environ['DATABASE_FILENAME'] = db
    app = create_app(__name__)
    app.secret_key = 'secret'
    sess = Session(app)
    app.run(debug = True)


if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.secret_key = 'super secret key'
    sess.init_app(app)
    app.run(debug=True)
