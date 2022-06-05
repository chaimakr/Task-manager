import unittest
from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from app import  add_user, add_task, update_task ,get_tasks, detele_task, update_task_state
from Models import Todo, User
#to run the test:
#coverage run -m unittest Unit\unit_tests.py
db = SQLAlchemy()
def create_test_app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "xxxxxxtestdatabasexxx"
    # Dynamically bind SQLAlchemy to application
    db.init_app(app)
    app.app_context().push() # this does the binding
    return app

class MyTest(TestCase):
    def create_app(self):
        return create_test_app()

    def setUp(self):

        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

        