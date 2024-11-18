from flask_restful import Resource
from flask import request, url_for
from flask_wtf.csrf import CSRFError
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from models import db
from models.users import Users
from models.employments import Employment
from decorators.api_login_required import api_login_required
from schemas.sch_user_personal_info import PersonalInformationSchema
from schemas.sch_user_employment_info import EmploymentInformationSchema


class AdminUpdateUser(Resource):
    @api_login_required
    def put(self, user_id):
        try:
            if not user_id:
                return {'error': 'Missing user ID.'}, 400

            data = request.get_json()
            employment_info_schema = EmploymentInformationSchema()

            try:
                validated_data = employment_info_schema.load(data)

            except ValidationError as err:
                error_messages = []
                for field, messages in err.messages.items():
                    for message in messages:
                        error_messages.append(
                            {'field': field, 'message': message}
                        )
                return {'errors': error_messages}, 400

            user = Users.query.filter_by(id=user_id).first()

            if not user:
                return {'error': 'User not found.'}, 404

            employment = Employment.query.filter_by(user_id=user.id).first()

            if employment:
                for field in ['employee_id', 'company', 'position', 'hired_date']:
                    if field in validated_data:
                        setattr(employment, field, validated_data[field])
            else:
                new_records = Employment(
                    user_id=user.id,
                    employee_id=validated_data['employee_id'],
                    company=validated_data['company'],
                    position=validated_data['position'],
                    hired_date=validated_data['hired_date']
                )
                db.session.add(new_records)

            db.session.commit()

            return {
                'success': 'User information updated successfully.',
                'redirect': url_for('admin_user_view', user_id=user_id)
            }, 200

        except CSRFError:
            return {'error': 'CSRF token missing or invalid.'}, 403

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'An error occurred while updating the user.'}, 500

        except Exception as e:
            return {'error': 'An unexpected error occurred.'}, 500

    @api_login_required
    def patch(self, user_id):
        try:
            if not user_id:
                return {'error': 'Missing user ID.'}, 400

            data = request.get_json()
            personal_info_schema = PersonalInformationSchema()

            try:
                validated_data = personal_info_schema.load(data, partial=True)

            except ValidationError as err:
                error_messages = []
                for field, messages in err.messages.items():
                    for message in messages:
                        error_messages.append(
                            {'field': field, 'message': message})
                return {'errors': error_messages}, 400

            user = Users.query.filter_by(id=user_id).first()

            if not user:
                return {'error': 'User not found.'}, 404

            for field, value in validated_data.items():
                setattr(user, field, value)

            db.session.commit()

            return {
                'success': 'User information updated successfully.',
                'redirect': url_for('admin_user_view', user_id=user_id)
            }, 200

        except CSRFError:
            return {'error': 'CSRF token missing or invalid.'}, 403

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'An error occurred while updating the user.'}, 500

        except Exception as e:
            return {'error': 'An unexpected error occurred.'}, 500
