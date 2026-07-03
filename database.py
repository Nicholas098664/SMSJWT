import sqlite3

def get_db_connection():
    conn = sqlite3.connect('easy.db')
    conn.row_factory = sqlite3.Row
    return conn

def users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,

        failed_attempts INTEGER DEFAULT 0,
        locked_until TEXT DEFAULT NULL
    )
    """)

    conn.commit()
    conn.close()

    

def students(): 
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
    student_id  INTEGER PRIMARY KEY AUTOINCREMENT ,
    name  TEXT NOT NULL,
    age INTEGER NOT NULL,
    grade TEXT NOT NULL
    )
    """) 
    conn.commit()
    conn.close()  




def init_audit_table():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()  




def log_action(user_id, action):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (user_id, action)
        VALUES (?, ?)
    """, (user_id, action))

    conn.commit()
    conn.close()    