import mysql.connector
from mysql.connector import Error


# class Connection:
#     def __init__(self):
#         self.connection = create_connection("localhost", "root", "", "sm_app")


# def create_connection(host_name, user_name, user_password):
#     con = None
#     try:
#         con = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password
#         )
#         print("Connection to MySQL DB successful")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#
#     return con


def create_connection(host_name, user_name, user_password, db_name):
    con = None
    try:
        con = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return con


# def create_database(con, query):
#     cursor = con.cursor()
#     try:
#         cursor.execute(query)
#         print("Database created successfully")
#     except Error as e:
#         print(f"The error '{e}' occurred")

def execute_query(con, query):
    cursor = con.cursor()
    try:
        cursor.execute(query)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query_w_val(con, query, val):
    cursor = con.cursor()
    try:
        cursor.execute(query, val)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def select_query_w_val(con, query, val):
    cursor = con.cursor()
    try:
        cursor.execute(query, val)
        print("Select successfully")
        return cursor.fetchall()
    except Error as e:
        print(f"The error '{e}' occurred")


# connection = create_connection("localhost", "root", "")
# create_database_query = "CREATE DATABASE sm_app"
# create_database(connection, create_database_query)
connection = create_connection("localhost", "root", "", "sm_app")

# CREATE TABLES

create_users_table = """
CREATE TABLE IF NOT EXISTS Users (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  password TEXT NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

create_projects_table = """
CREATE TABLE IF NOT EXISTS Projects (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

create_users_projects_table = """
CREATE TABLE IF NOT EXISTS UsersProjects (
  user_id INT NOT NULL, 
  project_id INT NOT NULL, 
  PRIMARY KEY (user_id, project_id),
  FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
"""

create_tasks_table = """
CREATE TABLE IF NOT EXISTS Tasks (
  id INT AUTO_INCREMENT, 
  title VARCHAR(200) UNIQUE, 
  description TEXT,
  mode VARCHAR(10) NOT NULL,
  bug BOOLEAN NOT NULL,
  bonus BOOLEAN NOT NULL,
  initial_date DATETIME NOT NULL,
  due_date DATETIME NOT NULL,
  severity int NOT NULL,
  in_progress BOOLEAN NOT NULL,
  done BOOLEAN NOT NULL,
  project_id INT NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (project_id) REFERENCES Projects(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
"""

create_assignees_table = """
CREATE TABLE IF NOT EXISTS Assignees (
  task_id INT NOT NULL, 
  user_id INT NOT NULL,
  PRIMARY KEY (task_id, user_id),
  FOREIGN KEY (task_id) REFERENCES Tasks(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
"""


# # EXECUTE CREATE TABLES
# execute_query(connection, create_users_table)
# execute_query(connection, create_projects_table)
# execute_query(connection, create_users_projects_table)
# execute_query(connection, create_tasks_table)
# execute_query(connection, create_assignees_table)

# INSERT
def insertUser(name, password):
    sql = "INSERT INTO Users ('name', 'password') VALUES (%s, %s)"
    val = (name, password)

    execute_query_w_val(connection, sql, val)


def insertProject(user_name, project_name):
    sql = "INSERT INTO Projects ('name') VALUES (%s)"
    val = project_name

    execute_query_w_val(connection, sql, val)

    user_id = selectUserID(user_name)

    project_id = selectProjectID(project_name)

    sql = "INSERT INTO UsersProjects VALUES (%s, %s)"
    val = (user_id, project_id)

    execute_query_w_val(connection, sql, val)


def insertTask(project_name, title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done,
               assignees):
    project_id = selectProjectID(project_name)

    sql = "INSERT INTO Tasks VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done, project_id)

    execute_query_w_val(connection, sql, val)

    task_id = selectTaskID(title)

    for name in assignees:
        user_id = selectUserID(name)

        sql = "INSERT INTO Assignees VALUES (%s, %s)"
        val = (task_id, user_id)

        execute_query_w_val(connection, sql, val)


# DELETE
def deleteUser(name):
    delete_comment = "DELETE FROM Users WHERE name = $s"
    val = name
    execute_query_w_val(connection, delete_comment, val)


def deleteProject(name):
    delete_comment = "DELETE FROM Projects WHERE name = $s"
    val = name
    execute_query_w_val(connection, delete_comment, val)


def deleteTask(title):
    delete_comment = "DELETE FROM Tasks WHERE title = $s"
    val = title
    execute_query_w_val(connection, delete_comment, val)


# UPDATE
def updateUser(old_name, name, password):
    user_id = selectUserID(old_name)

    sql = "UPDATE Users SET name = %s, password = %s WHERE id = $s"
    val = (name, password, user_id)

    execute_query_w_val(connection, sql, val)


def updateProject(old_project_name, project_name):
    project_id = selectProjectID(old_project_name)

    sql = "UPDATE Project SET name = %s, WHERE id = $s"
    val = (project_name, project_id)
    execute_query_w_val(connection, sql, val)


def updateTask(old_title, title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done,
               assignees):
    task_id = selectTaskID(old_title)

    sql = "UPDATE Project SET name = %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE id = $s"
    val = (title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done, task_id)
    execute_query_w_val(connection, sql, val)

    delete_comment = "DELETE FROM Assignees WHERE task_id = $s"
    val = task_id
    execute_query_w_val(connection, delete_comment, val)

    for name in assignees:
        user_id = selectUserID(name)

        sql = "INSERT INTO Assignees VALUES (%s, %s)"
        val = (task_id, user_id)

        execute_query_w_val(connection, sql, val)


# SELECT ID
def selectUserID(name):
    sql = "SELECT id FROM Users WHERE name = %s"
    val = name

    return select_query_w_val(connection, sql, val)


def selectProjectID(name):
    sql = "SELECT id FROM Projects WHERE name = %s"
    val = name

    return select_query_w_val(connection, sql, val)


def selectTaskID(title):
    sql = "SELECT id FROM tasks WHERE title = %s"
    val = title

    return select_query_w_val(connection, sql, val)


def selectUser(name):
    sql = "SELECT * FROM Users WHERE name = %s"
    val = name

    return select_query_w_val(connection, sql, val)


def selectProject(name):
    sql = "SELECT * FROM Projects WHERE name = %s"
    val = name

    return select_query_w_val(connection, sql, val)


def selectTask(title):
    sql = "SELECT * FROM Tasks WHERE title = %s"
    val = title

    return select_query_w_val(connection, sql, val)


def selectAssigneesName(title):
    task_id = selectTaskID(title)

    sql = "SELECT Users.name FROM Assignees INNER JOIN Users Users.id = Assignees.user_id WHERE task_id = %s"
    val = task_id

    return select_query_w_val(connection, sql, val)

