from connect import create_connection, database
# import subprocess
from create_table import create_table
from connect import create_connection, database
from seed import generate_users, generate_tasks, insert_users_table,insert_status_table,insert_tasks_table
from queries import * # get_userid, get_statusid, get_tasks
import random

# subprocess.run('python', 'create_table.py')


if __name__ ==  '__main__':
    NUMBER_USERS = 3
    NUMBER_TASKS = 10
    statuses = [('new',), ('in progress',), ('completed',)]
    
    print("/n")
    print("/n")
    print("=======================Creating data structure=======================")    
    with open('create_tables.sql', 'r') as f:
        sql_create_tables = f.read()

    with create_connection(database) as conn:                                #creating database and tables
        if conn and sql_create_tables is not None:
            er_message = create_table(conn, sql_create_tables) 
        else:
            print("Error! no connection to database or create_tables.sql missed")
        
    if er_message is not None:
        print(f"Error commiting SQL script: {er_message}")
    else:                                                                    #filling tables with data
        print("=======================Data structure created!=======================")
        while True:
            print("""
                1. Fill database with Fake data via Faker
                2. Get all task by user_id
                3. Get tasks by statuses (in this status, or all except in this status)
                4. Get tasks Qty by statuses
                5. Enter description to find in DB
                6. Get user tasks by statuses
                7. Get users and Qty of their tasks, or get users without tasks
                8. Get all tasks of users with inputed email (@example.com)
                9. Update status by task_id
                10. Add new task
                11. Delete task by task_id
                12. find users by email
                13. Update user name by user_id

            """)
            user_input = input("Choose number what to do or print close or exit to stop: ")
            try:
                match user_input:                                                                  # case for bot commands
                    case "close"|"exit":                                                        # close або exit: Закрити програму.
                        print("Good bye!")
                        break
                    case "1":
                        fake_users = generate_users(NUMBER_USERS)
                        with create_connection(database) as conn:                            #insert users into table users
                            last_user_id = insert_users_table(conn, fake_users)

                        with create_connection(database) as conn:                            #insert statuses into table status
                            insert_status_table(conn,statuses)
                            
                        # print(f"last_user_id: {last_user_id}")
                        with create_connection(database) as conn:                            #gets all user_id from users
                            users_id = get_userid(conn)

                        with create_connection(database) as conn:                            #gets all status_id from statuses
                            statuses_id = get_statusid(conn)

                        for user_id in users_id:
                            fake_tasks = generate_tasks(NUMBER_TASKS)
                            for fake_task in fake_tasks:
                                status_id = random.choice(statuses_id)
                                task = (status_id[0],user_id[0],fake_task[0],fake_task[1])
                                with create_connection(database) as conn:                    #insert tasks into tasks for user_id
                                    insert_tasks_table(conn, task)
                        print("Data filled sucessfully!")
                    case "2":
                    #Отримати всі завдання певного користувача. Використайте SELECT для отримання завдань конкретного користувача за його user_id.
                        user_id =  input("input user_id: ")
                        with create_connection(database) as conn:                              
                            print(get_tasks_by_userid(conn, int(user_id)))
                    case "3":
                    #Вибрати завдання за певним статусом. Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
                        # Отримати всі завдання, які ще не завершено. Виберіть завдання, чий статус не є 'завершено'.
                        notin = input("Do you want to include or exclude tasks with status (keep empty for include or enter yes for exclude)): ")
                        status =  input("input status (new, in progress, completed): ")
                        with create_connection(database) as conn:                              
                            print(get_task_by_status(conn, status, bool(notin)))
                    case "4":
                    # Отримати кількість завдань для кожного статусу. Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.                        
                        with create_connection(database) as conn:                           
                            print(get_tasks_qty_by_statuses(conn))
                    case "5":
                    # Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
                        with create_connection(database) as conn:           
                            description = input("Enter description to find all tasks with it, or press enter to find tasks with empty description: ")
                            print(get_tasks_by_description(conn, description))
                    case "6":
                    # Вибрати користувачів та їхні завдання, які є у статусі 'in progress'. 
                    #   Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
                        with create_connection(database) as conn:                              
                            status =  input("input status (new, in progress, completed) to find all users and their tasks in this status: ")
                            print(get_usertasks_by_status(conn,status))
                    case "7":
                    # Отримати користувачів та кількість їхніх завдань. 
                    #          Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
                    # Отримати список користувачів, які не мають жодного завдання. Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
                        with create_connection(database) as conn:                              
                            no_task = input("print 'yes' to to get users without tasks, or press enter to get users and Qty of their tasks: ")
                            print(get_users_by_tasks(conn, bool(no_task)))
                    case "8":
                    # Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. 
                    #          Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, 
                    #          чия електронна пошта містить певний домен (наприклад, '%@example.com').
                        with create_connection(database) as conn:
                            email_like = input("input email to find all tasks of users with this email (for example @example.com): ")
                            print(get_users_by_mail(conn,email_like))
                    case "9":                    
                    # Оновити статус конкретного завдання. Змініть статус конкретного завдання на 'in progress' або інший статус.
                        with create_connection(database) as conn:
                            task_id = input("input task_id to update status (for example 15):")
                            status = input("input new status (new, in progress, completed) for a task: ")
                            print(update_task_status(conn, status, int(task_id)))

                    case "10":
                    # Додати нове завдання для конкретного користувача. Використайте INSERT для додавання нового завдання.
                        with create_connection(database) as conn:                              
                            status_id = input("inpt status id for new tasks (1 - new, 2 - in progress, 3 - completed):")
                            user_id = input("input user_id for new task (for example from 1 to 3):")
                            title = input ("input task title: ")
                            description = input("input description:")
                            print(add_task_by_user(conn,int(status_id), int(user_id), title, description))
                    case "11":
                    # Видалити конкретне завдання. Використайте DELETE для видалення завдання за його id.
                        with create_connection(database) as conn:
                            task_id=input("input task_id to delete:")
                            print(del_task(conn,int(task_id)))
                    case "12":
                    # Знайти користувачів з певною електронною поштою. Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
                        with create_connection(database) as conn:
                            email = input("input email to find user:")
                            print(find_userbymail(conn,email))
                
                    case "13":
                    # Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
                        with create_connection(database) as conn:                              
                            user_id = input("input user_id for update user's name (for example from 1 to 3):")
                            new_user_name = input("input new user name for user:")
                            print(update_user(conn,int(user_id),new_user_name))
            except Exception as ex:
                print(ex)
                    











