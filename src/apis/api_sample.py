from flask import jsonify, request, url_for
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from models import db
from models.schedules import Schedules
from helpers.get_user_session import get_user_from_session


class SampleApi(Resource):
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
            except IntegrityError:
                db.session.rollback()
            else:
                db.session.commit()

        return jsonify({'redirect': url_for('time_schedule')})
