from functools import wraps
from flask import redirect, session, url_for

from models.users import Users


def redirect_to_dashboard(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get("user_id")
        if user_id:
            user = Users.query.filter_by(id=user_id).first()
            if user and user.role == 'admin':
                return redirect(url_for('admin'))
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function
