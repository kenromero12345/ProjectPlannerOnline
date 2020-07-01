import mysql.connector
from mysql.connector import Error

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
connection = None


def connect():
    global connection
    connection = createConnection("localhost", "root", "", "sm_app")


def createConnection(host_name, user_name, user_password, db_name):
    con = None
    try:
        con = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        # deleteAllTables(con)
        executeQuery(con, createUsersTable)
        executeQuery(con, createProjectsTable)
        executeQuery(con, createMembersTable)
        executeQuery(con, createTasksTable)
        executeQuery(con, createAssigneesTable)
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return con


# connection = createConnection("localhost", "root", "", "sm_app")

# def create_database(con, query):
#     cursor = con.cursor()
#     try:
#         cursor.execute(query)
#         print("Database created successfully")
#     except Error as e:
#         print(f"The error '{e}' occurred")

def executeQuery(con, query):
    cursor = con.cursor()
    try:
        cursor.execute(query)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def executeQueryWVal(con, query, val):
    cursor = con.cursor()
    try:
        cursor.execute(query, val)
        con.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def selectQueryWVal(con, query, val):
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
# connection = create_connection("localhost", "root", "", "sm_app")

# CREATE TABLES

createUsersTable = """
CREATE TABLE IF NOT EXISTS Users (
  id INT AUTO_INCREMENT, 
  name VARCHAR(50) NOT NULL, 
  password TEXT NOT NULL,
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

createProjectsTable = """
CREATE TABLE IF NOT EXISTS Projects (
  project_id INT AUTO_INCREMENT, 
  name VARCHAR(100) NOT NULL, 
  user_id INT NOT NULL,
  PRIMARY KEY (project_id),
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
"""

createMembersTable = """
CREATE TABLE IF NOT EXISTS Members (
  user_id INT NOT NULL,
  project_id INT NOT NULL,
  PRIMARY KEY (user_id, project_id),
  FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
"""

createTasksTable = """
CREATE TABLE IF NOT EXISTS Tasks (
  id INT AUTO_INCREMENT, 
  title VARCHAR(200) NOT NULL, 
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
  FOREIGN KEY (project_id) REFERENCES Projects(project_id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
"""

createAssigneesTable = """
CREATE TABLE IF NOT EXISTS Assignees (
  task_id INT NOT NULL, 
  user_id INT NOT NULL,
  PRIMARY KEY (task_id, user_id),
  FOREIGN KEY (task_id) REFERENCES Tasks(id) ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE = InnoDB
"""


# # # EXECUTE CREATE TABLES
# executeQuery(connection, createUsersTable)
# executeQuery(connection, createProjectsTable)
# executeQuery(connection, createUsersProjectsTable)
# executeQuery(connection, createTasksTable)
# executeQuery(connection, createAssigneesTable)


# INSERT
def insertUser(name, password):
    sql = "INSERT INTO Users (name, password) VALUES (%s, %s)"
    val = (name, password)
    # print(name, password)
    executeQueryWVal(connection, sql, val)


def insertProject(user_name, project_name):
    # print(selectUser(user_name)[0][0])
    # selectUser(user_name)[0][0]
    sql = "INSERT INTO Projects (name, user_id) VALUES (%s, %s)"
    val = (project_name, selectUser(user_name)[0][0])

    executeQueryWVal(connection, sql, val)


def insertMember(user_id, user_name, project_name):
    # print(selectUser(user_name)[0][0])
    # selectUser(user_name)[0][0]
    member_id = selectUser(user_name)[0][0]
    # if user_id != member_id:
    sql = "INSERT INTO Members (project_id, user_id) VALUES (%s, %s)"
    val = (selectProjectID(project_name, user_id)[0][0], member_id)

    executeQueryWVal(connection, sql, val)


def insertTask(project_name, title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done,
               assignees, user_id):
    project_id = selectProjectID(project_name, user_id)[0][0]
    # print(project_id)
    # print(title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done, project_id)

    sql = "INSERT INTO Tasks (title, description, mode, bug, bonus, initial_date, due_date, severity, " \
          "in_progress, done, project_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    # val = (title, description, mode, bug, bonus, str(initial_date) + "00:00:00", str(due_date) + "00:00:00", severity,
    #        in_progress, done, project_id)
    print(in_progress)
    val = (title, description, mode, bug, bonus, initial_date, due_date, severity,
           in_progress, done, project_id)

    executeQueryWVal(connection, sql, val)

    task_id = selectTaskID(title)

    for name in assignees:
        user_id = selectUserID(name)

        sql = "INSERT INTO Assignees VALUES (%s, %s)"
        val = (task_id, user_id)

        executeQueryWVal(connection, sql, val)


# DELETE
def deleteUser(name):
    delete_comment = "DELETE FROM Users WHERE name = %s"
    val = (name,)
    executeQueryWVal(connection, delete_comment, val)


def deleteProject(name):
    delete_comment = "DELETE FROM Projects WHERE name = %s"
    val = (name,)
    executeQueryWVal(connection, delete_comment, val)
    # executeQuery(connection, delete_comment)


def deleteMember(user_name, project_name, user_id):
    project_id = selectProjectID(project_name, user_id)
    user_id = selectUserID(user_name)

    delete_comment = "DELETE FROM Members WHERE project_id = %s and user_id = %s"
    val = (project_id, user_id)
    executeQueryWVal(connection, delete_comment, val)


def deleteTask(title, project_name, user_id):
    project_id = selectProjectID(project_name, user_id)

    delete_comment = "DELETE FROM Tasks WHERE title = %s and project_id = %s"
    val = (title, project_id)
    executeQueryWVal(connection, delete_comment, val)


# UPDATE
def updateUser(old_name, name, password):
    user_id = selectUserID(old_name)

    sql = "UPDATE Users SET name = %s, password = %s WHERE id = %s"
    val = (name, password, user_id)

    executeQueryWVal(connection, sql, val)


def updateProject(old_project_name, project_name):
    project_id = selectProjectID(old_project_name)

    sql = "UPDATE Project SET name = %s, WHERE id = %s"
    val = (project_name, project_id)
    executeQueryWVal(connection, sql, val)


def updateTask(old_title, title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done,
               assignees):
    task_id = selectTaskID(old_title)

    sql = "UPDATE Project SET name = %s, %s, %s, %s, %s, %s, %s, %s, %s, %s WHERE id = %s"
    val = (title, description, mode, bug, bonus, initial_date, due_date, severity, in_progress, done, task_id)
    executeQueryWVal(connection, sql, val)

    delete_comment = "DELETE FROM Assignees WHERE task_id = %s"
    val = task_id
    executeQueryWVal(connection, delete_comment, val)

    for name in assignees:
        user_id = selectUserID(name)

        sql = "INSERT INTO Assignees VALUES (%s, %s)"
        val = (task_id, user_id)

        executeQueryWVal(connection, sql, val)


# SELECT ID
def selectUserID(name):
    sql = "SELECT id FROM Users WHERE name = %s"
    val = (name,)

    return selectQueryWVal(connection, sql, val)


def selectProjectID(name, user_id):
    sql = "SELECT project_id FROM Projects WHERE name = %s AND user_id = %s"
    val = (name, user_id)

    return selectQueryWVal(connection, sql, val)


def selectTaskID(title):
    sql = "SELECT id FROM tasks WHERE title = %s"
    val = (title,)

    return selectQueryWVal(connection, sql, val)


def selectUser(name):
    sql = "SELECT * FROM Users WHERE name = %s"
    val = (name,)
    return selectQueryWVal(connection, sql, val)


def selectUserFromNameAndPW(name, password):
    sql = "SELECT * FROM Users WHERE name = %s AND password = %s"
    val = (name, password)
    return selectQueryWVal(connection, sql, val)


def selectProject(name):
    sql = "SELECT * FROM Projects WHERE name = %s"
    val = (name,)

    return selectQueryWVal(connection, sql, val)


def selectProjectFromUserID(user_id):
    # sql = "SELECT UsersProjects.project_id FROM UsersProjects WHERE UsersProjects.user_id = %s"
    # val = (user_id,)
    #
    # project_id = selectQueryWVal(connection, sql, val)

    # if not project_id:
    #     return [()]
    # else:
    #     project_id = project_id[0][0]

    sql = "SELECT Projects.name FROM Projects WHERE user_id = %s"
    val = (user_id,)

    return selectQueryWVal(connection, sql, val)


# def selectTask(title):
#     sql = "SELECT * FROM Tasks WHERE title = %s"
#     val = (title,)
#
#     return selectQueryWVal(connection, sql, val)


def selectTasks(name, user_id):
    project_id = selectProjectID(name, user_id)[0][0]
    print(project_id)
    sql = "SELECT * FROM Tasks WHERE project_id = %s"
    val = (project_id,)

    return selectQueryWVal(connection, sql, val)


def selectTasksAssignees(name, user_id):
    task_id = selectTasks(name, user_id)[0][0]

    sql = "SELECT user_id FROM Assignees WHERE task_id = %s"
    val = (task_id,)

    names = []

    for x in selectQueryWVal(connection, sql, val):
        sql = "SELECT name FROM Users WHERE user_id = %s"
        val = (x[0],)
        names.append(selectQueryWVal(connection, sql, val)[0][0])

    return names


def selectAssigneesName(title):
    task_id = selectTaskID(title)

    sql = "SELECT Users.name FROM Assignees INNER JOIN Users ON Users.id = Assignees.user_id WHERE task_id = %s"
    val = task_id

    return selectQueryWVal(connection, sql, val)


def selectMembers(name, user_id):
    project_id = selectProjectID(name, user_id)[0][0]
    # print(project_id)

    sql = "SELECT name FROM Members INNER JOIN Users ON Users.id = Members.user_id WHERE project_id = %s"
    val = (project_id,)
    #
    # sql = "SELECT user_id FROM Members WHERE Members.project_id = %s"
    # val = (project_id,)
    # user_ids = selectQueryWVal(connection, sql, val)
    # for x in user_ids:
    #
    # sql = "SELECT name FROM Users WHERE .project_id = %s"
    # val = (project_id,)
    #
    return selectQueryWVal(connection, sql, val)


def deleteAllTables(con):
    # sql = """
    #         DROP TABLE IF EXISTS Assignees;
    #         DROP TABLE IF EXISTS Tasks;
    #         DROP TABLE IF EXISTS Projects;
    #         DROP TABLE IF EXISTS Users;
    #         """
    #
    # executeQuery(connection, sql)

    sql = """
            DROP TABLE IF EXISTS Assignees;
            """

    executeQuery(con, sql)

    sql = """
            DROP TABLE IF EXISTS Tasks;
            """

    executeQuery(con, sql)

    sql = """
            DROP TABLE IF EXISTS Members;
            """

    executeQuery(con, sql)

    sql = """
            DROP TABLE IF EXISTS Projects;
            """

    executeQuery(con, sql)

    sql = """
            DROP TABLE IF EXISTS Users;
            """

    executeQuery(con, sql)
