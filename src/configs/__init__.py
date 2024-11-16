import os
from dotenv import load_dotenv

load_dotenv()


class Config():
    SECRET_KEY = os.getenv('SECRET_KEY')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    # SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_CLOUD_CONNECTION')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Session Configurations
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    # Flask Mail Configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    UPLOAD_FOLDER = 'src/static/assets/users/'
