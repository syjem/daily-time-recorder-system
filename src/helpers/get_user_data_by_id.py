from flask import flash, redirect, url_for
from models.users import Users


def get_user_data_by_id(user_id):
    user = Users.query.filter_by(id=user_id).first()

    if user:
        return user
    else:
        flash('User not found!'), 404
        return redirect(url_for('admin'))
