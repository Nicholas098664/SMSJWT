from flask import Blueprint, jsonify, request,url_for
from services.auth_service import signup, login
from auth.token_required import token_required
from admin_required import admin_required
from database import get_db_connection
from werkzeug.security import generate_password_hash

from email_utils import send_reset_email, verify_reset_token,generate_reset_token


auth_Tp = Blueprint("auth", __name__)


@auth_Tp.route("/signup", methods=["POST"])
def signup_route():

    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON data"}), 400

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username:
        return jsonify({"message": "Username is required"}), 400

    if not email:
        return jsonify({"message": "Email is required"}), 400

    if "@" not in email:
        return jsonify({"message": "Invalid email"}), 400

    if not password:
        return jsonify({"message": "Password is required"}), 400

    if len(password) < 8:
        return jsonify({"message": "Password must be at least 8 characters"}), 400

    result = signup({
        "username": username,
        "email": email,
        "password": password
    })

    return jsonify(result), (201 if result["success"] else 400)


@auth_Tp.route("/login", methods=["POST"])
def login_route():

    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON data"}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email:
        return jsonify({"message": "Email is required"}), 400

    if not password:
        return jsonify({"message": "Password is required"}), 400

    result = login(data)

    if result["success"]:
        return jsonify(result), 200

    return jsonify(result), 401



@auth_Tp.route("/makeadmin/<int:user_id>", methods=["GET"])
def make_admin(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET role = %s WHERE id = %s",
        ("admin", user_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    conn.close()

    return jsonify({
        "success": True,
        "message": "User is now an admin"
    }), 200



@auth_Tp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()
    email = data.get("email")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"message": "Email does not exist"}), 404

    
    token = generate_reset_token(email)

    
    reset_link = url_for("reset_page", token=token, _external=True)

    
    print("RESET LINK:", reset_link)

    return jsonify({
        "message": "Reset link generated (check server console)"
    }), 200

@auth_Tp.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):

    # 1. Verify token
    email = verify_reset_token(token)

    if not email:
        return jsonify({
            "success": False,
            "message": "Invalid or expired token."
        }), 400

    # 2. Get request data
    data = request.get_json()
    new_password = data.get("password")

    if not new_password:
        return jsonify({
            "success": False,
            "message": "Password is required."
        }), 400

    # 3. Password strength check (basic)
    if len(new_password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters long."
        }), 400

    # 4. Hash password
    hashed_password = generate_password_hash(new_password)

    # 5. DB connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # 6. Check if user exists
    cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({
            "success": False,
            "message": "User not found."
        }), 404

    # 7. Update password
    cursor.execute("""
        UPDATE users
        SET password = %s
        WHERE email = %s
    """, (hashed_password, email))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Password updated successfully."
    }), 200


@auth_Tp.route("/audit_logs")
@token_required
@admin_required
def audit_logs(payload):
    
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audit_logs ORDER BY id DESC")
    rows = cursor.fetchall()

    conn.close()

    logs = []

    for row in rows:
        logs.append({
            "id": row["id"],
            "user": row["user_id"],
            "action": row["action"],
            "time": row["timestamp"]   
        })

    return jsonify(logs)