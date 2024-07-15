import os

from flask import jsonify, request, url_for
from flask_restful import Resource
from marshmallow import ValidationError


from models import db
from decorators import api_login_required
from helpers import get_user_from_session, save_profile_upload, delete_previous_profile, is_file_type_allowed
from schemas import ProfileSetupSchema


class SampleApi(Resource):
    @api_login_required
    def get(self):
        return jsonify({'message': 'Sample message'})


class UploadUserProfile(Resource):

    @api_login_required
    def post(self):
        MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB

        if 'file' not in request.files or request.files['file'].filename == '':
            return {'error': 'No file part or no selected file'}, 400

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

            if user.image_file:
                delete_previous_profile(user.image_file)

            user.image_file = file_name
            db.session.commit()

        return jsonify({'image': url_for('static', filename=f'assets/upload/users/{file_name}')})


class DeleteUserProfile(Resource):
    @api_login_required
    def delete(self):
        user = get_user_from_session()

        try:
            if user.image_file:
                delete_previous_profile(user.image_file)
                user.image_file = ''
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'error': 'Failed to delete profile picture', 'message': str(e)}, 500

        return jsonify({'image': url_for('static', filename=f'assets/avatar.png')})


class SetupUserProfile(Resource):
    @api_login_required
    def post(self):
        schema = ProfileSetupSchema()
        try:
            data = schema.load(request.form)
        except ValidationError as err:
            response = jsonify({'error': err.messages})
            response.status_code = 400
            return response

        user = get_user_from_session()
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.set_password(data['password'])

        # Optional fields
        if 'position' in data:
            user.position = data['position']
        if 'employee_id' in data:
            user.employee_id = data['employee_id']

        db.session.commit()

        return jsonify({'success': 'Profile setup completed', 'redirect': url_for('dashboard')})
