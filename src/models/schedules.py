from models import db
from sqlalchemy import CheckConstraint, UniqueConstraint


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

    @db.validates('start_time', 'end_time')
    def validate_times(self, key, value):
        if not self.day_off and value is None:
            raise ValueError(f"{key} cannot be null unless it's a day off")
        return value
