import sqlite3

def open_connection():
    db_connection = sqlite3.connect("sqlite.db")
    db_cursor = db_connection.cursor()
    
    return [db_connection, db_cursor]