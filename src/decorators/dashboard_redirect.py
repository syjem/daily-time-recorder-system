from functools import wraps
from flask import redirect, session, url_for


def redirect_to_dashboard(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
