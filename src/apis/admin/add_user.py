import uuid

from flask import request, url_for
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError


from decorators.api_login_required import api_login_required
from schemas.sch_admin_add_user import AdminAddUserSchema
from models import db
from models.users import Users
from models.passwords import Passwords
from models.employments import Employment


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

        page = request.args.get('page', 1, type=int)
        total_users = Users.query.count()
        max_page = (total_users - 1) // 10 + 1

        if page > max_page:
            page = max_page

        return {'success': 'User added successfully.', 'redirect': url_for('admin', page=page)}, 201
