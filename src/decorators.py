from functools import wraps
from flask import flash, jsonify, redirect, session, url_for

from helpers import get_user_from_session
from models import Users


def login_required_and_get_user(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_user_from_session()
        if isinstance(user, Users):
            return f(user, *args, **kwargs)
        return user
    return decorated_function


def api_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            response = jsonify({'error': 'Authentication required'})
            response.status_code = 401
            return response
        return f(*args, **kwargs)
    return decorated_function


def redirect_to_dashboard(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_user_from_session()

        if not isinstance(user, Users):
            return user

        if user.role != 'admin':
            flash("Access denied: Admins only.", "danger")
            return redirect(url_for('index'))

        return f(user, *args, **kwargs)
    return decorated_function
