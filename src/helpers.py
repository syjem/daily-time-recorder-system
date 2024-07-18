import os
import secrets
import uuid

from flask_marshmallow import Marshmallow
from PIL import Image
from flask import flash, session, url_for
from models import Users
from config import Config


ma = Marshmallow()


def generate_confirmation_code(char=64):
    secret_key = ''.join(secrets.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)') for _ in range(char))

    return secret_key


def get_user_from_session():
    user_id = session.get('user_id')

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        flash('Invalid user ID.', 'danger')
        return None

    user = Users.query.filter_by(id=str(user_uuid)).first()

    if not user:
        flash('User not found.', 'danger')
        return None

    return user


def get_user_data(user):
    first_name = user.first_name
    last_name = user.last_name
    employee_id = user.employee_id
    email = user.email
    birthday = user.birthday
    position = user.position
    if user.image_file:
        image = url_for(
            'static', filename=f'assets/upload/users/{user.image_file}')
    else:
        image = url_for('static', filename=f'assets/avatar.png')

    return first_name, last_name, employee_id, email, birthday, position, image


def save_profile_upload(file):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(file.filename)
    file_name = random_hex + file_extension
    file_path = os.path.join(Config.UPLOAD_FOLDER, file_name)

    preferred_size = (500, 650)
    image = Image.open(file)
    image.thumbnail(preferred_size)

    image.save(file_path)

    return file_name


def delete_previous_profile(file_name):

    file = os.path.join('src', 'static', 'assets',
                        'upload', 'users', file_name)

    if os.path.exists(file):
        os.remove(file)


def is_file_type_allowed(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

    if '.' not in filename:
        return False

    # Split the filename at the last period to get the extension
    file_extension = filename.rsplit('.', 1)[1].lower()

    if file_extension in ALLOWED_EXTENSIONS:
        return True
    else:
        return False
