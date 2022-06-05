import os, sqlite3
from unittest import result

def adduser(username,password):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    cur.execute(
    "INSERT INTO USER (USERNAME,PASSWORD) VALUES (?,?);",(username,password,))
    connection.commit()

def verifyUser(username,password):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    user=cur.execute("SELECT * FROM USER WHERE USERNAME=?;", (username,)).fetchone()
    connection.commit()
    if(user==None):
        error="User not registered in database"
        return False,error
    if(user[2]!=password):
        error="Wrong password"
        return False,error
    return True,""

def fetch_user_by_username(username):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    user=cur.execute("SELECT * FROM USER WHERE USERNAME=?;", (username,)).fetchone()
    connection.commit()
    if(user==None):
        error="User not registered in database"
        return False,error
    return user

def fetch_allusers():
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    cur = connection.cursor()
    users=cur.execute("SELECT * FROM USER ;",).fetchall()
    connection.commit()
    return users