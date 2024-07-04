from flask import jsonify, request, url_for
from flask_restful import Resource


from models import db
from decorators import api_login_required
from helpers import get_user_from_session, save_profile_upload


class Sample_Api(Resource):
    @api_login_required
    def get(self):
        return jsonify({'message': 'Sample message'})


class Upload_User_Profile(Resource):
    @api_login_required
    def get(self):
        return jsonify({'message': 'Get request success'})

    @api_login_required
    def post(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            file_name = save_profile_upload(file)

            user = get_user_from_session()
            user.image_file = file_name
            db.session.commit()

        return jsonify({'image': url_for('static', filename=f'assets/upload/users/{file_name}')})
