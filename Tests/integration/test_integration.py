import pytest
import os
from app import create_app
from database import create_db
from flask_session import Session

#to run the test:
#coverage run -m pytest
#coverage run -m unittest "Tests\integration\test_integration.py"

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    database_filename = "test_database.db"
    create_db(database_filename)
    os.environ["DATABASE_FILENAME"] = database_filename



@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(__name__,test=True)
    flask_app.secret_key = 'strawhatt'
    flask_app.config.update({"TESTING":True,})
    testing_client = flask_app.test_client(use_cookies=True)
    context = flask_app.app_context()
    context.push()
    yield testing_client
    context.pop()

def test_home_get(test_client):

    # Given
    expected_status_code = 200
    expected_page_title = b"<h2>Choose your next step</h2>"
    # When
    response = test_client.get('/',follow_redirects=True)
    print(response.data)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_signIn_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Sign In</h1>"
    # When
    response = test_client.get('/login',follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_signIn_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Sign Up</h1>"
    # When
    response = test_client.get('/signup',follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data

def test_signUp_post(test_client):
    # Given
    expected_status_code = 200
    expected_page_redirection = b"Welcome to your Task Manager App"
    data_to_register={
                                        "username":"test",
                                        "password":"test"
                    }
    # When
    response = test_client.post('/signup',data=data_to_register,follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_redirection in response.data

def test_signIn_post_success(test_client):
    # Given
    expected_status_code = 200
    expected_page_message = b"Hi chaima"
    data_to_login={
                                        "username":"chaima",
                                        "password":"0000"
                }
    # When
    response = test_client.post('/login', data=data_to_login,follow_redirects=True)
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_message in response.data
    
def test_addtask_post(test_client):
    # Given
    expected_status_code = 200
    expected_page_message = b"Hi chaima"
    expected_task_content = b"TEST"
    data_to_add={
                                        "content":"TEST"
                                            }
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "chaima"
    # When
    response = test_client.post('/add',data=data_to_add,follow_redirects=True )
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_message in response.data
    assert expected_task_content in response.data

def test_updatetask_get(test_client):
    # Given
    expected_status_code = 200
    expected_page_title = b"<h1>Update Task</h1>"
    id_to_update=1
    with test_client.session_transaction() as session:
        session['logged_in'] = True
        session['username'] = "chaima"
    # When
    response = test_client.get(f'/update/{id_to_update}')
    # Then
    assert expected_status_code == response.status_code
    assert expected_page_title in response.data