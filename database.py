import sqlite3
import os

def create_db(database_filename):
    connection = sqlite3.connect(database_filename)
    cur = connection.cursor()
    cur.execute("DROP TABLE IF EXISTS Task")
    cur.execute("DROP TABLE IF EXISTS User")
    cur.execute(
        "CREATE TABLE Task (ID INTEGER PRIMARY KEY AUTO_INCREMENT, CONTENT TEXT NOT NULL, DATE TEXT NOT NULL, STATE INTEGER DEFAULT 0 , FOREIGN KEY(idowner) REFERENCES USER(id));")
    cur.execute(
        "CREATE TABLE User (ID INTEGER PRIMARY KEY, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL);")
    connection.commit()
    print("Done")
    connection.close()