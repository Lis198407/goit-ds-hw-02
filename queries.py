from sqlite3 import Error
from seed import generate_users, generate_tasks, insert_users_table,insert_status_table,insert_tasks_table
from queries import * # get_userid, get_statusid, get_tasks

def make_table_from_list(header_list:list,query_result:list)->str:
    # Find the maximum width for each column
    max_column_widths = [min(40, max(len(str(name)), max(len(str(value)) for value in column))) for name, column in zip(header_list, zip(*query_result))]

    # Print table header
    header = '| ' + ' | '.join(f'{name[:37]:<{width}}' + '...' if len(name) > 40 else f'{name:<{width}}' for name, width in zip(header_list, max_column_widths)) + ' |'
    line = '-' * len(header)
    message = f'{line}\n{header}\n{line}\n'

    # Print rows
    for row in query_result:
        row_str = '| ' + ' | '.join(f'{str(value)[:37]:<{width}}' + '...' if len(str(value)) > 40 else f'{str(value):<{width}}' for value, width in zip(row, max_column_widths)) + ' |'
        message += f'{row_str}\n'
    return message

def get_userid(conn, user = None):
    users = []
    try:
        cur = conn.cursor()
        if user is None:
            sql ="SELECT id FROM users"
            cur.execute(sql)
        else:
            sql = "SELECT id FROM users where name=?;"
            cur.execute(sql, (user,))
        users = cur.fetchall()
    except Error as e:
        print(f"Error in select_1.py in get_userid: {e}")
    finally:
        cur.close()
    return users

def get_statusid(conn, status = None):
    statuses = []
    try:
        cur = conn.cursor()
        if status is None:
            sql ="SELECT id FROM status"
            cur.execute(sql)
        else:
            sql = "SELECT id FROM status where name=?;"
            cur.execute(sql, (status,))            
        statuses = cur.fetchall()
    except Error as e:
        print(f"Error in select_1.py in get_statusid: {e}")
    finally:
        cur.close()
    return statuses

#Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
def get_tasks_by_userid(conn, user_id:int):
    try:   
        sql = "SELECT * FROM tasks WHERE user_id = ?;"
        cur = conn.cursor()
        cur.execute(sql, (user_id,))            
        results = cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)

    except Error as e:
        message = f"Error in queries.py in get_tasks_by_userid: {e}"
    finally:
        cur.close()
    return message


#Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
# Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
def get_task_by_status(conn, status: str, notin: bool = False):
    try:
        if notin:
            sql = "SELECT t.title, s.name FROM tasks t JOIN status s ON t.status_id = s.id WHERE NOT s.name = ?;"
        else:
            sql = "SELECT t.title, s.name FROM tasks t JOIN status s ON t.status_id = s.id WHERE s.name = ?;"
        cur = conn.cursor()
        cur.execute(sql, (status,))            
        results = cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)
    except Error as e:
        message = f"Error in queries.py in get_tasks_qty_by_statuses: {e}"
    finally:
        cur.close()
    return message


# Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
def get_tasks_qty_by_statuses(conn):
    try:   
        sql = "SELECT s.name, COUNT(t.id) FROM tasks t JOIN status s ON t.status_id = s.id GROUP BY s.name"
        cur = conn.cursor()
        cur.execute(sql)            
        results = cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)
    except Error as e:
        message = f"Error in queries.py in get_tasks_qty_by_statuses: {e}"
    finally:
        cur.close()
    return message


# Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
def get_tasks_by_description(conn, description:str =""):
    try:
        cur = conn.cursor()
        if description == "":
            sql = "SELECT t.title, t.description FROM tasks t WHERE t.description = ''"
            cur.execute(sql)            
        else:
            description = "%"+description+"%"
            sql = "SELECT t.title, t.description FROM tasks t WHERE t.description LIKE ?"
            cur.execute(sql,(description,))            
        results= cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)
    except Error as e:
        message = f"Error in queries.py in get_tasks_by_description: {e}"
    finally:
        cur.close()
    return message


# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
#          Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
def get_usertasks_by_status(conn,status:str):
    try:   
        sql = "SELECT s.name, t.title, u.fullname FROM tasks t JOIN status s ON t.status_id = s.id JOIN users u ON t.user_id = u.id WHERE s.name = ?;"
        cur = conn.cursor()
        cur.execute(sql, (status,))            
        results = cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)
    except Error as e:
        message = f"Error in queries.py in get_usertasks_by_status: {e}"
    finally:
        cur.close()
    return message


# Отримати користувачів та кількість їхніх завдань. 
#          Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
# Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
def get_users_by_tasks(conn, no_task:bool = False):
    try:
        cur = conn.cursor()
        if no_task:
            sql = "SELECT u.fullname FROM users u WHERE u.id NOT IN (SELECT t.user_id FROM tasks t GROUP BY t.user_id)"
        else:
            sql = "SELECT u.fullname,COUNT(t.id) FROM users u LEFT JOIN tasks t ON t.user_id = u.id GROUP BY u.fullname;"
        cur.execute(sql)            
        results = cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)
    except Error as e:
        message = f"Error in queries.py in get_users_by_tasks: {e}"
    finally:
        cur.close()
    return message

# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. 
#          Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, 
#          чия електронна пошта містить певний домен (наприклад, '%@example.com').
def get_users_by_mail(conn,email_like:str)->str:
    try:   
        email_like = "%"+email_like+"%"
        sql = "SELECT u.fullname,u.email,t.title FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE ?;"
        cur = conn.cursor()
        cur.execute(sql,(email_like,))            
        results = cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)
    except Error as e:
        message = f"Error in queries.py in get_users_by_mail: {e}"
    finally:
        cur.close()
    return message

# Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
def update_task_status(conn,status:str, task_id:int)->str:
    try:    
        sql = "UPDATE tasks SET status_id = (select s.id FROM status s WHERE s.name =?) WHERE id = ?;"
        cur = conn.cursor()
        cur.execute(sql,(status,task_id))
        conn.commit()        
        message = "Updated succesfully!"
    except Error as e:
        message = f"Error in queries.py in update_task_status: {e}"
    finally:
        cur.close()
    return message

# Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
def add_task_by_user(conn,status_id:int, user_id:int, title:str, description:str)->str:
    try:   
        sql = """INSERT INTO tasks (status_id,user_id,title,description) VALUES(?,?,?,?);
        """
        cur = conn.cursor()
        cur.execute(sql,(status_id,user_id,title,description))
        conn.commit()
        message = "Inserted succesfully!"
    except Error as e:
        message = f"Error in queries.py in add_task_by_user: {e}"
    finally:
        cur.close()
    return message


# Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
def del_task(conn,id:int)->str:
    try:   
        sql = """DELETE FROM tasks WHERE id = ?;
        """
        cur = conn.cursor()
        cur.execute(sql,(id,))
        conn.commit()
        message = "Deleted succesfully!"
    except Error as e:
        message = f"Error in queries.py in del_task: {e}"
    finally:
        cur.close()
    return message


# Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
def find_userbymail(conn,email:str)->str:
    try:
        email = "%"+email+"%"
        cur = conn.cursor()
        sql = "SELECT fullname,email FROM users where email LIKE ?;"
        cur.execute(sql, (email,))
        results = cur.fetchall()
        description_list = [description[0] for description in cur.description]
        message = make_table_from_list(description_list,results)
    except Error as e:
        message = f"Error in queries.py in find_userbymail: {e}"
    finally:
        cur.close()
    return message

# Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
def update_user(conn,user_id:int,new_user_name:str) ->str:
    try:  
        sql = "UPDATE users SET fullname = ? WHERE id = ?;"
        cur = conn.cursor()
        cur.execute(sql,(new_user_name,user_id))
        conn.commit()
        message = "Updated succesfully!"
    except Error as e:
        message = f"Error in queries.py in update_user: {e}"
    finally:
        cur.close()
    return message