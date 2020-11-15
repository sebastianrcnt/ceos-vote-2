from .database import connect

def create_user(email, password, name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO USER VALUES (?, ?, ?)", (email, password, name))
    conn.commit()

def verify_user(email, password):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM USER WHERE email=? AND password=?", (email, password))
    user = cur.fetchone()
    if user:
        return True
    return False

def get_user_by_email(email):
    conn = connect()
    cur = conn.cursor()
    print(email)
    cur.execute("SELECT * FROM USER WHERE email=?", (email,))
    user = cur.fetchone()
    return user
