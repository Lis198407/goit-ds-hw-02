from faker import Faker
import sqlite3

def generate_users(number_users) -> tuple():
    fake_users = []                

    fake_data = Faker()
    for _ in range(number_users):
        fake_user = (fake_data.name(),fake_data.email())
        fake_users.append(fake_user)
    return fake_users

def generate_tasks(number_tasks) -> tuple():
    fake_tasks = []

    fake_data = Faker()

    word_list = ["ToDo task","achieve a mission","create new product","finish job","in this month","in 3 days","at monday 9 o'clock","till the EOW","gather information", "finish project", "get the result", "in 2 hours", "minimize costs"]
    for _ in range(number_tasks):
        fake_task = (fake_data.sentence(nb_words = 2,variable_nb_words = False, ext_word_list = word_list),fake_data.text())
        fake_tasks.append(fake_task)
    return fake_tasks

# users  - list of tuples
def insert_users_table(conn, users):
    sql = '''
        INSERT INTO users(fullname, email) VALUES(?,?);
        '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, users)
        conn.commit()
        id = cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error in seed.py -- insert_users_table: {e}")
    finally:
        cur.close()
    return id

# statusses  - list of tuples
def insert_status_table(conn,statuses):
    sql = '''
        INSERT INTO status(name) VALUES(?);
        '''
    cur = conn.cursor()
    try:
        cur.executemany(sql, statuses)
        conn.commit()
        id = cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error in seed.py -- insert_status_table: {e}")
    finally:
        cur.close()
    return id

def insert_tasks_table(conn,tasks):
    sql = '''
        INSERT INTO tasks(status_id,user_id,title,description) VALUES(?,?,?,?);
        '''
    cur = conn.cursor()
    try:
        cur.execute(sql, tasks)
        conn.commit()
        id = cur.lastrowid
    except sqlite3.Error as e:
        print(f"Error in seed.py -- insert_status_table: {e}")
    finally:
        cur.close()
    return id