import os

from flask import jsonify, request, url_for
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import exc


from models import db, Employment, Schedules
from decorators import api_login_required
from helpers import get_user_from_session, save_profile_upload, delete_previous_profile, is_file_type_allowed
from schemas import PersonalInformationSchema, EmploymentInformationSchema


class SampleApi(Resource):
    @api_login_required
    def get(self):
        return jsonify({'message': 'Sample message'})

    def post(self):
        data = request.get_json()
        user = get_user_from_session()

        for schedule in data:
            day = schedule['day']
            day_off = schedule['day_off']
            shift_type = schedule.get('shift_type', None)

            new_schedule = Schedules(
                user_id=user.id,
                day=day,
                day_off=day_off,
                shift_type=shift_type
            )

            try:
                db.session.merge(new_schedule)
            except exc.IntegrityError:
                db.session.rollback()
            else:
                db.session.commit()

        return jsonify({'redirect': url_for('time_schedule')})


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

            if user.image_file:
                message = 'Profile picture updated.'
                delete_previous_profile(user.image_file)
            else:
                message = 'Uploaded.'

            user.image_file = file_name
            db.session.commit()

        return jsonify({'image': url_for('static', filename=f'assets/upload/users/{file_name}'), 'message': message})

    @api_login_required
    def delete(self):
        user = get_user_from_session()

        if user.image_file:
            delete_previous_profile(user.image_file)
            user.image_file = ''
            db.session.commit()

        return jsonify({'src': url_for('static', filename=f'assets/avatar.png'), 'message': 'Profile picture removed.'})


class PersonalInformation(Resource):
    @api_login_required
    def post(self):
        data = request.form

        personal_info_schema = PersonalInformationSchema()
        try:
            validated_data = personal_info_schema.load(data)

        except ValidationError as err:
            error_messages = []
            for field, messages in err.messages.items():
                for message in messages:
                    error_messages.append({'field': field, 'message': message})
            return {'errors': error_messages}, 400

        user = get_user_from_session()
        user.first_name = validated_data['first_name']
        user.last_name = validated_data['last_name']
        user.email = validated_data['email']
        user.birthday = validated_data['birthday']

        db.session.commit()

        return jsonify({'success': 'Information updated.'})

    @api_login_required
    def patch(self):
        return jsonify({'success': 'Personal information updated successfully'})

    @api_login_required
    def delete(self):
        pass


class EmploymentInformation(Resource):
    @api_login_required
    def post(self):
        data = request.form

        employment_info_schema = EmploymentInformationSchema()
        try:
            validated_data = employment_info_schema.load(data)
        except ValidationError as err:
            error_messages = []
            for field, messages in err.messages.items():
                for message in messages:
                    error_messages.append({'field': field, 'message': message})
            return {'errors': error_messages}, 400

        company = validated_data['company']
        employee_id = validated_data['employee_id']
        position = validated_data['position']
        hired_date = validated_data['hired_date']

        user = get_user_from_session()
        employment = Employment.query.filter_by(user_id=user.id).first()

        if employment:
            employment.employee_id = validated_data['employee_id']
            employment.position = validated_data['position']
            employment.company = validated_data['company']
            employment.hired_date = validated_data['hired_date']
            db.session.commit()
        else:
            new_user_employment = Employment(
                user_id=user.id, company=company, employee_id=employee_id, position=position, hired_date=hired_date)
            db.session.add(new_user_employment)
            db.session.commit()

        return jsonify({'success': 'Employment information has been updated.'})
