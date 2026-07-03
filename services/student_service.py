from database import get_db_connection


def addstudent(data):
    conn =get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students ( name, age,grade)
    VALUES (?,?,?)
    
    """, (data["name"],data["age"],data["grade"]))

    conn.commit()
    conn.close()

    return True


def Allstudents():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
     

def getstudent(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
    "SELECT * FROM students WHERE student_id = ?",
    (student_id,)
    )
    row = cursor.fetchone()
   
    if row:
        return dict(row) 
    conn.close()

def delete(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE student_id = ?",
        (student_id,)
    )

    conn.commit()

    deleted = cursor.rowcount > 0

    conn.close()

    return deleted


def update(student_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET name = ?, age = ?, grade = ?
        WHERE student_id = ?
    """, (data["name"], data["age"], data["grade"], student_id))

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated

def getbyname(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE name = ?", (name,))
        
        
    student = cursor.fetchone()
    return student
    
    cursor.close()
    conn.close()

def counter():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    result = cursor.fetchone()

    conn.close()

    return result[0] if result else 0