import uuid
import secrets

from flask_marshmallow import Marshmallow

ma = Marshmallow()


def format_datetime(date):
    day = date.day
    return date.strftime(f'%A, %B {day}, %I:%M %p')


def generate_token():
    token = str(uuid.uuid4())
    return token


def generate_confirmation_code(char=64):
    secret_key = ''.join(secrets.choice(
        'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*(-_=+)') for _ in range(char))

    return secret_key
