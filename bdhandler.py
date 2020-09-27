import sqlite3 as sql


def createdb():                                 #Создание базы данных и таблици, в программе не оспользуется
    conn = sql.connect('taskstable.db')
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE tasks(id integer, id_user integer, message text, image text, PRIMARY KEY (id, id_user))")
    conn.commit()


def addtask(task):                              #Добавление записи о задаче в
    conn = sql.connect('taskstable.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (id, id_user, message, image) VALUES (?, ?, ?, ?)", task)
    conn.commit()


def deltask(taskid):
    conn = sql.connect('taskstable.db')
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks WHERE id = ? AND id_user = ?", taskid)
    conn.commit()


def showall(user):
    conn = sql.connect('taskstable.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, message, image FROM tasks WHERE id_user = ?", (user,))
    rows = cursor.fetchall()
    return rows


def cleardb():
    conn = sql.connect('taskstable.db')
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM tasks")
    conn.commit()


def numberoftasks(user):
    conn = sql.connect('taskstable.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE id_user = ?", (user,))
    return str(cursor.fetchone()[0])

def photopath(taskid):
    conn = sql.connect('taskstable.db')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT image FROM tasks WHERE id = ? AND id_user = ?", taskid)
    path = str(cursor.fetchone()[0])
    return path