import os
import secrets
import uuid

from PIL import Image
from flask import flash, session
from models import Users
from config import Config
# from app import app


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


# def save_profile_upload(file):
#     random_hex = secrets.token_hex(8)
#     _, file_extension = os.path.splitext(file.filename)
#     file_name = random_hex + file_extension
#     file_path = os.path.join(
#         app.root_path, "static/assets/upload/users/", file_name)

#     preferred_size = (200, 200)
#     image = Image.open(file)
#     image.thumbnail(preferred_size)

#     image.save(file_path)

#     return file_name
