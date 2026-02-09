import sqlite3

DB_PATH = "data/applications.db"

def get_connection():
    return sqlite3.connect(DB_PATH)