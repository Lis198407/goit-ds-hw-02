from sqlite3 import Error
from connect import create_connection, database

def create_table(conn, sql):  #creates Table via SQL in SQLite DB
    try:
        c = conn.cursor()
        c.executescript(sql)
        conn.commit
    except Error as er:
        return er