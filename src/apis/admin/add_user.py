import uuid

from flask import request, url_for
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash


from models import db
from models.users import Users
from models.passwords import Passwords
from models.employments import Employment
from schemas.sch_admin_add_user import AdminAddUserSchema
from decorators.api_login_required import api_login_required


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

        user_id = str(uuid.uuid4())

        email_is_not_unique = Users.query.filter_by(
            email=validated_data['email']).first()

        if email_is_not_unique:
            return {'email_error': 'Email is already in use.'}, 400

        user = Users(
            id=user_id,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            birthday=validated_data['birthday']
        )

        password_entry = Passwords(
            user_id=user.id,
            current_password_hash=generate_password_hash(
                validated_data['password'])
        )

        employment_entry = Employment(
            user_id=user.id,
            position=validated_data['position']
        )

        try:
            db.session.add(user)
            db.session.add(password_entry)
            db.session.add(employment_entry)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'error': 'An error occurred while adding the user.'}, 400

        total_users = Users.query.count()
        max_page = (total_users - 1) // 10 + 1

        redirect_url = ''

        page = request.args.get('page', type=int)
        if page:
            if page > max_page:
                page = max_page
                redirect_url = url_for('admin', page=page)
        else:
            redirect_url = url_for('admin')

        return {
            'success': 'User added successfully.',
            'redirect': redirect_url
        }, 201
