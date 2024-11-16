from flask_restful import Resource
from flask import request
from flask_wtf.csrf import CSRFError
from sqlalchemy.exc import SQLAlchemyError

from models import db


class AdminUpdateUser(Resource):

    def patch(self, user_id):
        try:
            if not user_id:
                return {'error': 'Missing user ID.'}, 400

            data = request.form

        except CSRFError:
            return {'error': 'CSRF token missing or invalid.'}, 403

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'An error occurred while deleting the user.'}, 500

        except Exception as e:
            return {'error': 'An unexpected error occurred.'}, 500
