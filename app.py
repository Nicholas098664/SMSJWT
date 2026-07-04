from flask import Flask, render_template
from flask_cors import CORS

from routes.auth_route import auth_Tp
from routes.student_route import student_Tp

from database import users, students, init_audit_table

app = Flask(__name__)
CORS(app)

# =========================
# BLUEPRINTS
# =========================
app.register_blueprint(student_Tp)
app.register_blueprint(auth_Tp)

# =========================
# ROUTES
# =========================
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/register")
def register_page():
    return render_template("Register.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/forgot-password")
def forgot_password_page():
    return render_template("forgotpassword.html")

@app.route("/reset-password/<token>")
def reset_page(token):
    return render_template("Resetpassword.html", token=token)

@app.route("/audit")
def audit():
    return render_template("audit.html")


# =========================
# SAFE DB INIT (RUN ON IMPORT)
# =========================
try:
    users()
    students()
    init_audit_table()
    print("✅ DB initialized")
except Exception as e:
    print("❌ DB Error:", e)


# =========================
# MAIN (LOCAL ONLY)
# =========================
if __name__ == "__main__":
    app.run(debug=True)