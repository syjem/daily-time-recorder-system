from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError

from models import db
from models.employments import Employment
from helpers.get_user_session import get_user_from_session
from decorators.api_login_required import api_login_required
from schemas.sch_user_employment_info import EmploymentInformationSchema


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
