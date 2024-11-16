from flask import url_for


def get_logged_in_user_data(user):
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    birthday = user.birthday
    role = user.role
    if user.avatar:
        avatar = url_for(
            'static', filename=f'assets/users/{user.avatar}')
    else:
        avatar = None

    return first_name, last_name,  email, birthday, role, avatar
