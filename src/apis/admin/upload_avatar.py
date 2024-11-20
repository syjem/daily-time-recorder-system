import os
from flask_restful import Resource
from flask import jsonify, request, url_for

from models import db
from models.users import Users
from decorators.api_login_required import api_login_required
from helpers.upload_files import is_file_type_allowed, save_profile_upload, delete_previous_profile


class AdminUploadUserAvatar(Resource):
    @api_login_required
    def post(self, user_id):
        MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

        user = Users.query.filter_by(id=user_id).first()

        if not user:
            return {'error': 'User not found!'}, 404

        if 'avatar' not in request.files or request.files['avatar'].filename == '':
            return {'error': 'No file selected'}, 400

        avatar = request.files['avatar']

        if not is_file_type_allowed(avatar.filename):
            return {'error': 'File type not allowed'}, 400

        # determine the size of the uploaded file
        avatar.seek(0, os.SEEK_END)
        file_size = avatar.tell()
        avatar.seek(0, 0)

        if file_size > MAX_FILE_SIZE:
            return {'error': 'File size exceeds limit (max 1MB).'}, 400

        if avatar:
            file_name = save_profile_upload(avatar)

            if user.avatar:
                message = 'Avatar successfully updated.'
                delete_previous_profile(user.avatar)
            else:
                message = 'Avatar successfully uploaded.'

            user.avatar = file_name
            db.session.commit()

        return jsonify(
            {
                'avatar': url_for('static', filename=f'assets/users/{file_name}'), 'message': message
            }
        )

    @api_login_required
    def delete(self, user_id):
        user = Users.query.filter_by(id=user_id).first()

        if not user:
            return {'error': 'User not found!'}, 404

        if user.avatar:
            delete_previous_profile(user.avatar)
            user.avatar = None

            db.session.commit()

        return {
            'avatar': url_for('static', filename='assets/avatar.png'),
            'message': 'Successfully removed user avatar.'
        }
