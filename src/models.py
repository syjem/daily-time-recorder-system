import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True,
                   default=uuid.uuid4, unique=True, nullable=False)
    employee_id = db.Column(db.String(30))
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(200))
    hashed_password = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
