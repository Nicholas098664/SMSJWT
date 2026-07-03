from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message

from itsdangerous import SignatureExpired, BadSignature

SECRET_KEY = "YOUR_SECRET_KEY"

serializer = URLSafeTimedSerializer(SECRET_KEY)

def generate_reset_token(email):
    return serializer.dumps(email, salt="password-reset")




def send_reset_email(mail, email):

    token = generate_reset_token(email)

    reset_link = f"http://127.0.0.1:5000/reset-password/{token}"

    html = f"""
    <html>
    <body style="font-family:Arial;background:#f4f4f4;padding:30px;">

        <div style="max-width:600px;margin:auto;background:white;padding:30px;border-radius:10px;">

            <h2 style="color:#2c3e50;">
                Student Management System
            </h2>

            <p>Hello,</p>

            <p>
                We received a request to reset your password.
            </p>

            <p style="text-align:center;margin:40px;">

                <a href="{reset_link}"
                   style="
                    background:#007BFF;
                    color:white;
                    padding:15px 25px;
                    text-decoration:none;
                    border-radius:6px;
                    font-size:18px;
                   ">

                   Reset Password

                </a>

            </p>

            <p>
                This link expires in <strong>1 hour</strong>.
            </p>

            <p>
                If you didn't request this password reset,
                simply ignore this email.
            </p>

            <hr>

            <small>
                Student Management System
            </small>

        </div>

    </body>
    </html>
    """

    msg = Message(
        subject="Reset Your Password",
        recipients=[email],
        html=html
    )

    mail.send(msg)




def verify_reset_token(token):
    try:
        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=3600  # 1 hour
        )
        return email

    except SignatureExpired:
        return None

    except BadSignature:
        return None    