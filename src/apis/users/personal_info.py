from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from models import db
from helpers.get_user_session import get_user_from_session
from decorators.api_login_required import api_login_required
from schemas.sch_user_personal_info import PersonalInformationSchema


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
