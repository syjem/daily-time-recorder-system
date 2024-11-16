from models import db
from sqlalchemy import CheckConstraint, UniqueConstraint


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
