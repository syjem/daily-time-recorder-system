from functools import wraps
from flask import jsonify, session


def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            response = jsonify({'error': 'Authentication required'})
            response.status_code = 401
            return response
        return f(*args, **kwargs)
    return decorated_function