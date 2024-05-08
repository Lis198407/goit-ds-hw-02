import sqlite3
from contextlib import contextmanager

database = "./ds_hw_02.db"

@contextmanager
def create_connection(db_file):   #creates connection to SQLite db file
    conn = sqlite3.connect(db_file)    
    yield conn
    conn.rollback()
    conn.close()
