from models import db
from werkzeug.security import generate_password_hash, check_password_hash


class Passwords(db.Model):
    __tablename__ = 'passwords'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)
    current_password_hash = db.Column(db.String(128), nullable=False)
    old_password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.current_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.current_password_hash, password)
