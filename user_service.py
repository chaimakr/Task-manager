import os, sqlite3

def add_user(username,password):
    database_filename = os.environ.get('DATABASE_FILENAME')
    connection = sqlite3.connect(database_filename, check_same_thread=False)
    connection.execute(
    "INSERT INTO Users (USERNAME,PASSWORD) VALUES (?,?);",(username,password,))
    connection.commit()