import os
print("DATABASE_URL FOUND:", os.environ.get("DATABASE_URL") is not None)
import psycopg
from psycopg.rows import dict_row


def get_db_connection():

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        conn = psycopg.connect(
            database_url,
            row_factory=dict_row
        )
    else:
        conn = psycopg.connect(
            host="localhost",
            dbname="sms_db",
            user="postgres",
            password="123456",
            port=5432,
            row_factory=dict_row
        )

    return conn

def users():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
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
    student_id SERIAL PRIMARY KEY,
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
        id SERIAL PRIMARY KEY ,
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
        VALUES (%s, %s)
    """, (user_id, action))

    conn.commit()
    conn.close()    






if __name__ == "__main__":
    users()
    students()
    init_audit_table()

    print("Tables created successfully!")