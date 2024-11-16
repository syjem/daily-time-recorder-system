from functools import wraps

from helpers.get_user_session import get_user_from_session
from models.users import Users


def login_required_and_get_user(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_user_from_session()
        if isinstance(user, Users):
            return f(user, *args, **kwargs)
        return user
    return decorated_function
