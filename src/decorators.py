from functools import wraps
from flask import flash, redirect, session, url_for

from helpers import get_user_from_session


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You'll need to login first to access this page.", 'danger')
            return redirect(url_for("sign_in"))
        return f(*args, **kwargs)
    return decorated_function


def login_required_and_get_user(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You'll need to login first to access this page.", 'danger')
            return redirect(url_for("sign_in"))

        user = get_user_from_session()
        if user is None:
            return redirect(url_for('sign_in'))

        return f(user, *args, **kwargs)
    return decorated_function


def logout_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            flash("You're already logged in.", 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def email_session_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            flash('Access denied', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def redirect_to_dashboard(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def redirect_to_profile_page(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect(url_for('profile'))
        return f(*args, **kwargs)
    return decorated_function
