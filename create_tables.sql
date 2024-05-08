--  drops users if exsist in DB and creates table users
        DROP TABLE IF EXISTS users;
        CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fullname VARCHAR(100),
                email VARCHAR(100) UNIQUE
        );

--  drops status if exsist in DB and creates table status
        DROP TABLE IF EXISTS status;
        CREATE TABLE IF NOT EXISTS status (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(50) UNIQUE                   
        );

--  drops tasks if exsist in DB and creates table tasks
        DROP TABLE IF EXISTS tasks;
        CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                status_id INTEGER,
                user_id INTEGER,
                title VARCHAR(100),
                description TEXT,
                FOREIGN KEY (status_id) REFERENCES status (id)
                FOREIGN KEY (user_id) REFERENCES users (id)
                    ON DELETE CASCADE
        );