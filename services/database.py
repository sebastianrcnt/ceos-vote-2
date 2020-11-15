import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect():
    connection = sqlite3.connect("database.db")
    connection.row_factory = dict_factory
    return connection


def queryone(sql):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchone()

def queryall(sql):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

def executeone(sql, context):
    # context: tuple
    # sql: text
    pass
