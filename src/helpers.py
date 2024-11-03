import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone

from flask_marshmallow import Marshmallow
from PIL import Image
from flask import flash, make_response, redirect, session, url_for
from models import db, Users, Employment, Tokens
from config import Config


ma = Marshmallow()


def generate_confirmation_code(char=64):
    secret_key = ''.join(secrets.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)') for _ in range(char))

    return secret_key


def get_user_from_session():
    user_id = session.get('user_id')
    if not user_id:
        flash('User session is missing. Please log in.', 'danger')
        return redirect(url_for('sign_in'))

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        flash('Invalid user ID.', 'danger')
        return redirect(url_for('sign_in'))

    user = Users.query.filter_by(id=str(user_uuid)).first()
    if not user:
        flash("Access denied: You do not have the necessary permissions to view this page.", 'danger')
        return redirect(url_for('sign_in'))

    return user


def get_user_data(user):
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    birthday = user.birthday
    role = user.role
    if user.image_file:
        image = url_for(
            'static', filename=f'assets/upload/users/{user.image_file}')
    else:
        image = url_for('static', filename=f'assets/avatar.png')

    return first_name, last_name,  email, birthday, role, image


def get_employment_data(user):
    user = Employment.query.filter_by(user_id=user.id).first()
    if user:
        employee_id = user.employee_id
        company = user.company
        hired_date = user.hired_date
        position = user.position

        return employee_id, company, hired_date, position

    return '', '', '', ''


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


def generate_token():
    token = str(uuid.uuid4())
    return token


def handle_remember_me_token(user_id):
    tkn = Tokens.query.filter_by(user_id=user_id).first()

    if not tkn:
        remember_token = generate_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        new_token = Tokens(
            user_id=user_id, token=remember_token, expires_at=expires_at)
        db.session.add(new_token)
        db.session.commit()
    else:
        remember_token = tkn.token

    # Set the token in a secure cookie
    response = make_response(redirect(url_for('dashboard')))
    response.set_cookie('remember_token', remember_token, secure=True,
                        httponly=True, samesite='Lax', max_age=30*24*60*60)
    return response


def format_datetime(date):
    day = date.day
    return date.strftime(f'%A, %B {day}, %I:%M %p')
