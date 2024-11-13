import os
import uuid

from flask import jsonify, request, url_for, redirect
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import exc
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask_wtf.csrf import CSRFError, validate_csrf


from models import db, Employment, Schedules, Users, Passwords, Tokens
from decorators import api_login_required
from helpers import get_user_from_session, save_profile_upload, delete_previous_profile, is_file_type_allowed
from schemas import AdminAddUserSchema, PersonalInformationSchema, EmploymentInformationSchema


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


class AdminAddUser(Resource):
    @api_login_required
    def post(self):
        data = request.form

        admin_add_user_schema = AdminAddUserSchema()
        try:
            validated_data = admin_add_user_schema.load(data)

        except ValidationError as err:
            error_messages = []
            for field, messages in err.messages.items():
                for message in messages:
                    error_messages.append({'field': field, 'message': message})
            return {'errors': error_messages}, 400

        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        position = validated_data['position']
        birthday = validated_data['birthday']
        email = validated_data['email']
        password = validated_data['password']

        user_id = str(uuid.uuid4())

        user = Users(
            id=user_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            birthday=birthday
        )

        password_entry = Passwords(
            user_id=user.id,
            current_password_hash=generate_password_hash(password)
        )

        employment_entry = Employment(
            user_id=user.id,
            position=position
        )

        try:
            db.session.add(user)
            db.session.add(password_entry)
            db.session.add(employment_entry)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'error': 'User with this email already exists.'}, 400

        return {'success': 'User added successfully.', 'redirect': url_for('admin')}, 201


class AdminDeleteUser(Resource):

    def delete(self, user_id):
        try:
            data = request.form
            user_id = data['user_id']

            if not user_id:
                return {'error': 'Missing user ID.'}, 400

            user = Users.query.filter_by(id=user_id).first()

            if not user:
                return {'error': 'User not found!'}, 404

            Passwords.query.filter_by(user_id=user_id).delete()
            Employment.query.filter_by(user_id=user_id).delete()
            Tokens.query.filter_by(user_id=user_id).delete()
            Schedules.query.filter_by(user_id=user_id).delete()

            db.session.delete(user)
            db.session.commit()
            return {'success': 'User deleted successfully.', 'redirect': url_for('admin')}, 200

        except CSRFError:
            return {'error': 'CSRF token missing or invalid.'}, 403

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'An error occurred while deleting the user.'}, 500

        except Exception as e:
            return {'error': 'An unexpected error occurred.'}, 500
