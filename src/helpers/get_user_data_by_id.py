from flask import flash, redirect, url_for
from sqlalchemy.orm import joinedload
from models.users import Users


def get_user_data_by_id(user_id):
    user = Users.query.filter_by(id=user_id).options(
        joinedload(Users.employment)).first()

    if user:
        return user
    else:
        flash('User not found!', 'danger'), 404
        return redirect(url_for('admin'))
