from functools import wraps
from flask import flash, redirect, url_for
from helpers.get_user_session import get_user_from_session


def no_admin_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_user_from_session()

        if user and user.role == 'admin':
            flash('Page is for non admins only.', 'danger')
            return redirect(url_for('admin'))
        return f(*args, **kwargs)

    return decorated_function
