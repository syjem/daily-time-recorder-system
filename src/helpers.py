import os
import secrets
import uuid
from flask import flash, session, url_for
from models import Users
from config import Config


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

    user = Users.query.filter_by(id=str(user_uuid)).first()

    if not user:
        flash('User not found.', 'red')
        return None

    return user


def get_user_data(user):
    name = user.name
    email = user.email
    if user.image_file:
        replaced_folder = Config.UPLOAD_FOLDER.replace('src/', '')
        image = os.path.join(
            replaced_folder, os.path.basename(user.image_file))
    else:
        image = "https://github.com/shadcn.png"

    return name, email, image
