import sqlite3
import os

def create_db(database_filename):
    connection = sqlite3.connect(database_filename)
    cur = connection.cursor()
    cur.execute("DROP TABLE IF EXISTS Task")
    cur.execute("DROP TABLE IF EXISTS User")
    cur.execute(
        "CREATE TABLE Task (ID INTEGER PRIMARY KEY, CONTENT TEXT NOT NULL, DATE TEXT NOT NULL, STATE INTEGER DEFAULT 0 , IDOWNER INTERGER NOT NULL ,FOREIGN KEY(IDOWNER) REFERENCES User(ID));")
    cur.execute(
        "INSERT INTO Task (CONTENT,DATE,STATE,IDOWNER) VALUES ('pet namoussa','05/06/2022 14:36:05',1,3);"
        )
    cur.execute(
        "CREATE TABLE User (ID INTEGER PRIMARY KEY, USERNAME TEXT NOT NULL, PASSWORD TEXT NOT NULL);")
    cur.execute(
        "INSERT INTO User (USERNAME,PASSWORD) VALUES ('admin','admin'),('root','root'),('chaima','0000');")
    connection.commit()
    print("Done")
    connection.close()
#create_db("test.db")