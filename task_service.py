import sqlite3
import os

def fetch_by_id(id):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    task= cur.execute("SELECT * FROM TASK WHERE ID=?;", (id,)).fetchone()
    connection.close()
    return task

def fetch_alltasks_by_userid(id):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    tasks = cur.execute("SELECT * FROM Task WHERE idowner =? ;",(id,)).fetchall()
    connection.close()
    return tasks

def fetch_task_by_userid(id,idowner):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    tasks = cur.execute("SELECT * FROM Task WHERE id =? AND  idowner = ?;",(id,idowner,)).fetchone()
    connection.close()
    return tasks

def addtask(content,date,idowner):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
        "INSERT INTO Task (CONTENT,DATE,IDOWNER) VALUES (?,?,?);", (content,date,idowner,))
    print("task added")
    connection.commit()

def updatetask(content,date,idowner,id):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
        "UPDATE Task SET CONTENT=?, DATE=?, IDOWNER=? WHERE ID=?;", (content,date,idowner,id,))
    connection.commit()

def deletetask(id):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
        "DELETE FROM Task WHERE ID=?;",(id,))
    connection.commit()

def updatetaskstate(id,state):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
        "UPDATE Task SET STATE=? WHERE ID=?;",(state,id))
    connection.commit()
