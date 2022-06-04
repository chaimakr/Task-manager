import datetime
from ssl import create_default_context
from flask import Flask, render_template, url_for , request , redirect
from flask_sqlalchemy import SQLAlchemy
from database import create_db

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.String(200), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    state = db.Column(db.Integer, default=0)

def __repr__(self):
    return '<Task %r>' % self.id



@app.route('/', methods=['GET'])
def index():
    tasks = Todo.query.order_by(Todo.create_at).all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])
def add_task():
    task_content= request.form['content']
    new_task = Todo(content=task_content)

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



@app.route('/delete/<int:id>')
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


def main( db='test.db', create=False):
    if create:  
        create_db(db)
if __name__ == '__main__':
    app.run(debug=True)
