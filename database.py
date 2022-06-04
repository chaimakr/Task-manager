import sqlite3
import os

def create_db(database_filename):
    connection = sqlite3.connect(database_filename)
    cur = connection.cursor()
    cur.execute("DROP TABLE IF EXISTS Todo")
    cur.execute(
        "CREATE TABLE Todo (ID INTEGER PRIMARY KEY AUTO_INCREMENT, CONTENT TEXT NOT NULL, DATE TEXT NOT NULL, STATE INTEGER DEFAULT 0);")
    connection.commit()
    print("Done")
    connection.close()