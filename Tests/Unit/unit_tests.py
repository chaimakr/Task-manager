import sqlite3
from unittest import TestCase
from unittest.mock import patch
import os
from task_service import addtask, fetch_alltasks_by_userid, fetch_task_by_userid, fetch_by_id, updatetask, deletetask, updatetaskstate
from user_service import adduser, verifyUser, fetch_user_by_username ,fetch_allusers

os.environ['DATABASE_FILENAME'] = 'test.db'

#to run the test:
#coverage run -m unittest Tests\Unit\unit_tests.py
class TestAddUser(TestCase):
    @patch("user_service.sqlite3", spec=sqlite3)
    def test_addUser(self, mocked_object):
        # Given
        mock_execute= (mocked_object.connect.return_value.cursor.return_value.execute)
        # When
        adduser('test', 'test')
        # Then
        mock_execute.assert_called_once()

class TestVerifyUser(TestCase):
    def test_verifyUser_registred(self):
        #Given
        username='root'
        password='root'
        expected_result=True
        #When
        result,msg = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)
    def test_verifyUser_unregistered(self):
        #Given
        username='ahmed'
        password='0000'
        expected_result=False
        #When
        result,msg = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)
    def test_verifyUser_wrongPassword(self):
        #Given
        username='chaima'
        password='wrongpassword'
        expected_result=False
        #When
        result,msg = verifyUser(username,password)
        #Then
        self.assertEqual(expected_result,result)

class TestFetchById(TestCase):
    @patch("task_service.sqlite3")
    def test_task_fetchById_exists(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchone.return_value = (6,'pet namoussa','05/06/2022 14:36:05',1,4)
        expected_task = (6,'pet namoussa','05/06/2022 14:36:05',1,4)
        # When
        result_task = fetch_by_id(6)
        # Then
        self.assertEqual(expected_task, result_task)
    @patch("task_service.sqlite3")
    def test_task_fetchById_unexistant(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchone.return_value = None
        expected_task = None
        # When
        result_task = fetch_by_id(1)
        # Then
        self.assertEqual(expected_task, result_task)

class TestFetchAll(TestCase):
    @patch("user_service.sqlite3")
    def test_fetchAll_full(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchall.return_value = [("admin","admin"),("root","root"),("chaima","0000"),("chaimakr","0000"),("STRAWHATT4","0000")]
        expected_product = [("admin","admin"),("root","root"),("chaima","0000"),("chaimakr","0000"),("STRAWHATT4","0000")]
        # When
        result_product = fetch_allusers()
        # Then
        self.assertEqual(expected_product, result_product)

    @patch("user_service.sqlite3")
    def test_fetchAll_empty(self, mocked_object):
        # Given
        mocked_object.connect().cursor().execute().fetchall.return_value = None
        expected_users = None
        # When
        result_users = fetch_allusers()
        # Then
        self.assertEqual(expected_users, result_users)

class TestAddTask(TestCase):
    @patch("task_service.sqlite3", spec=sqlite3)
    def test_addtask(self, mocked_object):
        # Given
        mock_execute=(mocked_object.connect.return_value.execute)
        # When
        addtask('feed namoussa','05/06/2022 14:36:05',4)
        # Then
        mock_execute.assert_called_once()

    @patch("task_service.sqlite3", spec=sqlite3)
    def test_updatetask(self, mocked_object):
        # Given
        mock_execute=(mocked_object.connect.return_value.execute)
        # When
        updatetask('feed namoussa','05/06/2022 14:36:05',4,6)
        # Then
        mock_execute.assert_called_once()


class TestDeleteTask(TestCase):
    @patch("task_service.sqlite3", spec=sqlite3)
    def test_deleteProduct(self, mocked_object):
        # Given
        mock_execute=(mocked_object.connect.return_value.execute)
        # When
        deletetask(1)
        # Then
        mock_execute.assert_called_once()

class TestUpdateStateTask(TestCase):
    @patch("task_service.sqlite3", spec=sqlite3)
    def test_updatetaskstate(self, mocked_object):
        # Given
        mock_execute=(mocked_object.connect.return_value.execute)
        # When
        updatetaskstate(1,1)
        # Then
        mock_execute.assert_called_once()