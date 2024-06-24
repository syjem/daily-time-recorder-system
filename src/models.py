import uuid
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.String(64), primary_key=True, default=lambda: str(
        uuid.uuid4()), unique=True, nullable=False)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128), unique=True, nullable=False)
    image_file = db.Column(db.String(255))
    hashed_password = db.Column(db.String(255))
    remember_token = db.Column(db.String(255))

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def generate_remember_token(self):
        token = str(uuid.uuid4())
        self.remember_token = generate_password_hash(token)
        return token

    def check_remember_token(self, token):
        return check_password_hash(self.remember_token, token)
