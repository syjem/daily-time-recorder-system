import uuid
from sqlalchemy import func
from models import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True, default=lambda: str(
        uuid.uuid4()), unique=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    birthday = db.Column(db.Date)
    avatar = db.Column(db.String(32))
    role = db.Column(db.String(16), nullable=False, default='user')
    created_at = db.Column(db.DateTime(), server_default=func.now())

    passwords = db.relationship(
        'Passwords', backref='passwords', lazy='joined', cascade="all, delete-orphan", passive_deletes=True
    )
    employment = db.relationship(
        'Employment', backref='employment', lazy='joined', cascade="all, delete-orphan", passive_deletes=True
    )
    tokens = db.relationship(
        'Tokens', backref='tokens', lazy='joined', cascade="all, delete-orphan", passive_deletes=True
    )
    schedules = db.relationship(
        'Schedules', backref='schedules', lazy='joined', cascade="all, delete-orphan",
        passive_deletes=True
    )
