from datetime import datetime, timedelta, timezone

from flask import make_response, redirect, url_for

from models import db
from models.tokens import Tokens
from helpers import generate_token


def handle_remember_me_token(user):
    tkn = Tokens.query.filter_by(user_id=user.id).first()

    if not tkn:
        remember_token = generate_token()
        expires_at = datetime.now(timezone.utc) + timedelta(days=30)
        new_token = Tokens(
            user_id=user.id, token=remember_token, expires_at=expires_at)
        db.session.add(new_token)
        db.session.commit()
    else:
        remember_token = tkn.token

    if user.role != 'admin':
        response = make_response(redirect(url_for('dashboard')))
    else:
        response = make_response(redirect(url_for('admin')))

    # Set the token in a secure cookie
    response.set_cookie('remember_token', remember_token, secure=True,
                        httponly=True, samesite='Lax', max_age=30*24*60*60)
    return response
