from functools import wraps
from flask import flash, jsonify, redirect, session, url_for

from helpers import get_user_from_session


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash(
                "Access denied: You do not have the necessary permissions to view this page.", 'danger')
            return redirect(url_for("sign_in"))
        return f(*args, **kwargs)
    return decorated_function


def login_required_and_get_user(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash(
                "Access denied: You do not have the necessary permissions to view this page.", 'danger')
            return redirect(url_for("sign_in"))

        user = get_user_from_session()
        if user is None:
            return redirect(url_for('sign_in'))

        return f(user, *args, **kwargs)
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


# NOT FINAL: TO BE FIX...
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You'll need to login first to access this page.", 'danger')
            return redirect(url_for("sign_in"))

        user_role = session.get("user_role")

        if user_role != 'admin':
            flash("You don't have permission to access this page.", 'danger')
            return redirect(url_for("home"))

        return f(*args, **kwargs)
    return decorated_function
