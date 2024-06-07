import secrets
from functools import wraps
from flask import flash, redirect, session, url_for


def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("You'll need to login first to access this page.", 'orange')
            return redirect(url_for("sign_in"))
        return f(*args, **kwargs)
    return decorated_function


def logout_required(f):
    """
    Decorate routes to require logout.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            flash("You're already logged in.", 'blue')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def dashboard_redirect(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def email_session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("email") is None:
            flash('Access denied', 'red')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


def generate_confirmation_code(char=64):
    secret_key = ''.join(secrets.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)') for _ in range(char))

    return secret_key
