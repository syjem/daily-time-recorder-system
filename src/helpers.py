import secrets
import uuid
from flask import flash, session
from models import Users


def generate_confirmation_code(char=64):
    secret_key = ''.join(secrets.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)') for _ in range(char))

    return secret_key


def get_user_from_session():
    user_id = session.get('user_id')

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        flash('Invalid user ID.', 'red')
        return None

    user = Users.query.filter_by(id=user_uuid).first()

    if not user:
        flash('User not found.', 'red')
        return None

    return user


def get_user_data(user):
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    
    return first_name, last_name, email