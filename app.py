from flask import Flask, Blueprint
from flask_cors import  CORS
from database import users,students,init_audit_table
from routes.auth_route import auth_Tp
from routes.student_route import student_Tp
from flask import render_template
from flask_mail import Mail

app = Flask(__name__)
CORS(app)


app.register_blueprint(student_Tp)
app.register_blueprint(auth_Tp)



@app.route("/register")
def register_page():
    return render_template("Register.html")

@app.route("/login")
def login_page():
    return render_template("login.html")   

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/")
def landing():
    return render_template("Landing.html")


@app.route("/reset-password/<token>")
def reset_page(token):

    return render_template(
        "ResetPassword.html"
    )

@app.route("/audit")
def audit():
    return render_template("audit.html")








app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "richardsontommy0456@gmail.com"
app.config["MAIL_PASSWORD"] = "your_16_character_app_password"
app.config["MAIL_DEFAULT_SENDER"] = "richardsontommy0456@gmail.com"

mail = Mail(app)


if __name__ == ("__main__"):
    users()
    students()
    init_audit_table()
    app.run(debug = True)