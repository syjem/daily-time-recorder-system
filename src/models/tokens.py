from models import db
from sqlalchemy import func


class Tokens(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    token = db.Column(db.String(512))
    created_at = db.Column(db.DateTime(), server_default=func.now())
    expires_at = db.Column(db.DateTime())
