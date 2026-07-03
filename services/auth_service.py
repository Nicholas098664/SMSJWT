from database import get_db_connection,log_action
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from config import SECRET_KEY


def signup(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Every new user is a normal user
    role = "user"

    # Check if email already exists
    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return {
            "success": False,
            "message": "Email already exists"
        }

    hashed_password = generate_password_hash(password)

    # Save the role in the database
    cursor.execute("""
        INSERT INTO users (username, email, password, role)
        VALUES (?, ?, ?, ?)
    """, (username, email, hashed_password, role))

    conn.commit()
    conn.close()

    return {
        "success": True,
        "message": "User registered successfully"
    }


def login(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    email = data.get("email")
    password = data.get("password")

    cursor.execute("""
        SELECT * FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()

    # Check if user exists
    if not user:
        conn.close()
        return {
            "success": False,
            "message": "User not found"
        }

    # Check if account is locked
    if user["locked_until"]:
        locked_until = datetime.datetime.fromisoformat(user["locked_until"])

        if datetime.datetime.utcnow() < locked_until:
            conn.close()
            return {
                "success": False,
                "message": "Account is locked. Try again later."
            }

    # Check password
    if not check_password_hash(user["password"], password):

        attempts = user["failed_attempts"] + 1

        # Lock account after 5 failed attempts
        if attempts >= 5:

            locked_until = (
                datetime.datetime.utcnow() +
                datetime.timedelta(minutes=15)
            ).isoformat()

            cursor.execute("""
                UPDATE users
                SET failed_attempts = ?, locked_until = ?
                WHERE id = ?
            """, (attempts, locked_until, user["id"]))

            conn.commit()

            
            conn.close()

            return {
                "success": False,
                "message": "Too many failed attempts. Account locked for 15 minutes."
            }

        # Update failed attempts
        cursor.execute("""
            UPDATE users
            SET failed_attempts = ?
            WHERE id = ?
        """, (attempts, user["id"]))

        conn.commit()
        conn.close()

        return {
            "success": False,
            "message": f"Incorrect password. {5 - attempts} attempt(s) remaining."
        }

    # Password is correct - reset failed attempts and unlock account
    cursor.execute("""
        UPDATE users
        SET failed_attempts = 0,
            locked_until = NULL
        WHERE id = ?
    """, (user["id"],))

    conn.commit()
    log_action(user["id"], "Logged into the system")
    # Create JWT Token
    token = jwt.encode(
        {
            "user_id": user["id"],
            "email": user["email"],
            "role": user["role"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    conn.close()

    return {
        "success": True,
        "message": "Login successful",
        "token": token
    }





def log_action(user_id, action):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO audit_logs (user_id, action)
        VALUES (?, ?)
    """, (user_id, action))

    conn.commit()
    conn.close()