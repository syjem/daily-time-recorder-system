import uuid
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, func, UniqueConstraint
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


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


class Passwords(db.Model):
    __tablename__ = 'passwords'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    current_password_hash = db.Column(db.String(128), nullable=False)
    old_password_hash = db.Column(db.String(128))

    user = db.relationship(
        'Users', backref=db.backref('passwords', lazy='joined', passive_deletes=True))

    def set_password(self, password):
        self.current_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.current_password_hash, password)


class Employment(db.Model):
    __tablename__ = 'employment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    company = db.Column(db.String(128))
    employee_id = db.Column(db.String(32))
    position = db.Column(db.String(64), nullable=False)
    hired_date = db.Column(db.Date)

    __table_args__ = (
        UniqueConstraint('user_id', 'hired_date', name='uix_user_hired_date'),
        CheckConstraint('hired_date <= CURRENT_DATE',
                        name='chk_hired_date_not_future'),
    )

    user = db.relationship(
        'Users', backref=db.backref('employment', lazy='joined', passive_deletes=True))


class Tokens(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    token = db.Column(db.String(512))
    created_at = db.Column(db.DateTime(), server_default=func.now())
    expires_at = db.Column(db.DateTime())

    user = db.relationship(
        'Users', backref=db.backref('tokens', lazy='joined', passive_deletes=True))


class Schedules(db.Model):
    __tablename__ = 'schedules'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    day = db.Column(db.String(3), CheckConstraint(
        "day IN ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')"), nullable=False)
    day_off = db.Column(db.Boolean, nullable=False)
    shift_type = db.Column(db.String(8), CheckConstraint(
        "shift_type IN ('Opener', 'Regular', 'Closer')"))

    __table_args__ = (
        UniqueConstraint('user_id', 'day', name='uix_user_day'),
    )

    user = db.relationship(
        'Users', backref=db.backref('schedules', lazy='joined', passive_deletes=True))

    @db.validates('start_time', 'end_time')
    def validate_times(self, key, value):
        if not self.day_off and value is None:
            raise ValueError(f"{key} cannot be null unless it's a day off")
        return value
