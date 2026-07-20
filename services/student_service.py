from database import get_db_connection

def addstudent(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Get the last student_id
        cursor.execute("""
            SELECT student_id
            FROM students
            ORDER BY CAST(SUBSTRING(student_id FROM 4) AS INTEGER) DESC
            LIMIT 1
        """)

        last_student = cursor.fetchone()

        if last_student and last_student[0]:
            last_id = str(last_student[0]).strip().upper()
            number = int(last_id.replace("STU", ""))
            new_student_id = f"STU{number + 1:03d}"

        else:
            new_student_id = "STU001"

        cursor.execute("""
            INSERT INTO students (student_id, name, age, grade)
            VALUES (%s, %s, %s, %s)
        """, (
            new_student_id,
            data["name"],
            data["age"],
            data["grade"]
        ))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        import traceback
        traceback.print_exc()
        print("Add student error:", repr(e))
        return False

    finally:
        cursor.close()
        conn.close()

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
    "SELECT * FROM students WHERE student_id = %s",
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
        "DELETE FROM students WHERE student_id = %s",
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
        SET name = %s, age = %s, grade = %s
        WHERE student_id = %s
    """, (data["name"], data["age"], data["grade"], student_id))

    conn.commit()

    updated = cursor.rowcount > 0

    conn.close()

    return updated

def getbyname(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students WHERE name = %s", (name,))
        
        
    student = cursor.fetchone()
    return student
    
    cursor.close()
    conn.close()

def counter():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) AS total FROM students")

    result = cursor.fetchone()

    conn.close()

    return result["total"] if result else 0



