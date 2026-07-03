from functools import wraps
from flask import jsonify

def admin_required(f):

    @wraps(f)
    def wrapper(*args, **kwargs):

        payload = kwargs.get("payload")

        if payload.get("role") != "admin":
            return jsonify({
                "success": False,
                "message": "Admin access required"
            }), 403

        return f(*args, **kwargs)

    return wrapper