from ast import dump
from datetime import datetime
from click import launch
from flask import Flask, render_template, session, url_for , request , redirect 
from flask_session import Session
from database import create_db
from task_service import *
from user_service import *
from datetime import datetime

def create_app(name, test=False):
    if test:
        app = Flask(name,template_folder='../../Templates')
    else:
        app = Flask(name, template_folder='Templates')
    

    @app.route('/test', methods=['GET'])
    def test():
        return 'test'

    @app.route('/', methods=['GET'])
    def index():
        if 'logged_in' in session and session['logged_in']:
            tasks = fetch_alltasks_by_userid(session['iduser'])
            return render_template('index.html', tasks=tasks) 
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
        user = fetch_user_by_username(request.form['username'])
        print(user)
        if not(user) :
            return redirect(url_for('login_get'))
        if user:
            if verifyUser(request.form['username'],request.form['password']):
                session['logged_in'] = True
                session['username'] = user[1]
                session['iduser'] = user[0]
                #session['password'] = user.password
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
                adduser(username,password)
                return redirect('/')
            except:
                return 'there was an issue signing up'
        else:
            return render_template('signup.html')


        

    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        tasks = fetch_alltasks_by_userid(session['iduser'])
        return render_template('index.html', tasks=tasks)


    @app.route('/add', methods=['POST'])
    def add_task():
        iduser = session['iduser']
        task_content= request.form['content']
        task_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            print(task_content,task_date,iduser)
            addtask(task_content,task_date,iduser)
            return redirect('/')
        except:
            return 'there was an issue adding your task'  



    @app.route('/update/<int:id>', methods=['GET', 'POST'])
    def update_task(id):
        task = fetch_task_by_userid(id,session['iduser'])
        if request.method == 'POST':
            new_content = request.form['content']
            try:
                updatetask(new_content,task[2],session['iduser'],task[0])
                return redirect('/')
            except:
                return 'There was an issue updating your task'
        else:
            return render_template('update.html', task=task)



    @app.route('/delete/<int:id>')
    def detele_task(id):
        task_to_delete = fetch_task_by_userid(id,session['iduser'])
        try:
            deletetask(task_to_delete[0])
            return redirect('/')
        except:
            return 'There was a problem deleting that task'

    @app.route('/done/<int:id>')
    def update_task_state(id):
        iduser= session['iduser']
        task = fetch_task_by_userid(id,iduser)
        if task[3]== 0:
            new_task_state = 1
        else:  
            new_task_state = 0 
        try:
            updatetaskstate(id,new_task_state)
            return redirect('/')
        except:
            return 'There was an issue changing the state of your task'
    return app
    
def launch( db='test.db', create=False):
    if create:
        create_db(db)
    os.environ['DATABASE_FILENAME'] = db
    app = create_app(__name__)
    app.secret_key = 'strawhat'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess = Session(app)
    sess.init_app(app)    
    app.run(debug = True)

if __name__ == '__main__':
    app = launch()

