from functools import wraps
from flask import flash, redirect, url_for

from models.users import Users
from helpers.get_user_session import get_user_from_session


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_user_from_session()

        if not isinstance(user, Users):
            return user

        if user.role != 'admin':
            flash(
                "Access denied: You do not have the necessary permissions to view this page.", "danger")
            return redirect(url_for('index'))

        return f(user, *args, **kwargs)
    return decorated_function
