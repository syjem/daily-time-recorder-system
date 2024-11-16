import os
from flask import jsonify, request, url_for
from flask_restful import Resource

from models import db
from decorators.api_login_required import api_login_required
from helpers.get_user_session import get_user_from_session
from helpers.upload_files import is_file_type_allowed, save_profile_upload, delete_previous_profile


class ApiUserAvatar(Resource):
    @api_login_required
    def post(self):
        MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

        if 'file' not in request.files or request.files['file'].filename == '':
            return {'error': 'No file selected'}, 400

        file = request.files['file']

        if not is_file_type_allowed(file.filename):
            return {'error': 'File type not allowed'}, 400

        # determine the size of the uploaded file
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0, 0)

        if file_size > MAX_FILE_SIZE:
            return {'error': 'File size exceeds limit (max 1MB).'}, 400

        if file:
            file_name = save_profile_upload(file)

            user = get_user_from_session()

            if user.avatar:
                message = 'Profile picture updated.'
                delete_previous_profile(user.avatar)
            else:
                message = 'Uploaded.'

            user.avatar = file_name
            db.session.commit()

        return jsonify({'image': url_for('static', filename=f'assets/users/{file_name}'), 'message': message})

    @api_login_required
    def delete(self):
        user = get_user_from_session()

        if user.avatar:
            delete_previous_profile(user.avatar)
            user.avatar = ''
            db.session.commit()

        return jsonify({'src': url_for('static', filename='assets/avatar.png'), 'message': 'Profile picture removed.'})
