from functools import wraps
from flask import request, jsonify
import jwt

from config import SECRET_KEY

def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        try:
            
            if token.startswith("Bearer "):
                token = token.split(" ")[1]

            payload = jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )

            kwargs["payload"] = payload
            return f( *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token"}), 401

    return wrapper