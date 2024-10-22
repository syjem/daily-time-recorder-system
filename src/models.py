import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, func, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True, default=lambda: str(
        uuid.uuid4()), unique=True, nullable=False)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    birthday = db.Column(db.Date)
    image_file = db.Column(db.String(32))
    created_at = db.Column(db.DateTime(), server_default=func.now())


class Passwords(db.Model):
    __tablename__ = 'passwords'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id'), nullable=False)
    current_password_hash = db.Column(db.String(128), nullable=False)
    old_password_hash = db.Column(db.String(128))

    user = db.relationship(
        'Users', backref=db.backref('passwords', lazy='joined'))

    # Helper methods for password hashing
    def set_password(self, password):
        self.current_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.current_password_hash, password)


class Employment(db.Model):
    __tablename__ = 'employment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id'), nullable=False)
    company = db.Column(db.String(128), nullable=False)
    employee_id = db.Column(db.String(32))
    position = db.Column(db.String(64), nullable=False)
    hired_date = db.Column(db.Date)

    __table_args__ = (
        UniqueConstraint('user_id', 'hired_date', name='uix_user_hired_date'),
        CheckConstraint('hired_date <= CURRENT_DATE',
                        name='check_hired_date_not_future'),
    )

    user = db.relationship(
        'Users', backref=db.backref('employment', lazy='joined'))


class Tokens(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id'), nullable=False)
    token = db.Column(db.String(512))
    created_at = db.Column(db.DateTime(), server_default=func.now())
    expires_at = db.Column(db.DateTime())

    user = db.relationship(
        'Users', backref=db.backref('tokens', lazy='joined'))

    def generate_remember_token(self):
        token = str(uuid.uuid4())
        self.remember_token = token
        return token


class Schedules(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id'), nullable=False)
    day = db.Column(db.String(3), CheckConstraint(
        "day IN ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')"), nullable=False)
    day_off = db.Column(db.Boolean, nullable=False)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    __table_args__ = (
        UniqueConstraint('user_id', 'day', name='uix_user_day'),
    )

    user = db.relationship(
        'Users', backref=db.backref('schedules', lazy='joined'))

    @db.validates('start_time', 'end_time')
    def validate_times(self, key, value):
        if not self.day_off and value is None:
            raise ValueError(f"{key} cannot be null unless it's a day off")
        return value
