import uuid
from flask import flash, redirect, session, url_for
from models.users import Users


def get_user_from_session():
    user_id = session.get('user_id')
    if not user_id:
        flash('User session is missing. Please log in.', 'danger')
        return redirect(url_for('sign_in'))

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        flash('Invalid user ID.', 'danger')
        return redirect(url_for('sign_in'))

    user = Users.query.filter_by(id=str(user_uuid)).first()
    if not user:
        flash("Access denied: You do not have the necessary permissions to view this page.", 'danger')
        return redirect(url_for('sign_in'))

    return user
