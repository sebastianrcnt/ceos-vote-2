import sqlite3
from .database import connect

def vote(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE CANDIDATE SET voteCount = voteCount + 1 WHERE id = ?", (id,))
    conn.commit()

def get_candidate(id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM CANDIDATE WHERE id = ?", (id,))
    res = cur.fetchone()
    return res

def candidates():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM CANDIDATE")
    res = cur.fetchall()
    return res

def add_candidate(name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO CANDIDATE(name) VALUES (?)", (name,))
    res = cur.fetchall()
    conn.commit()
    return res

def clear_candidates():
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM CANDIDATE")
    conn.commit()

def reset_votes():
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE CANDIDATE SET voteCount = 0")
    conn.commit()
