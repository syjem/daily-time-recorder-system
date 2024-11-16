
from flask import request, url_for
from flask_restful import Resource
from flask_wtf.csrf import CSRFError
from sqlalchemy.exc import SQLAlchemyError

from models import db
from models.users import Users


class AdminDeleteUser(Resource):

    def delete(self, user_id):
        try:
            if not user_id:
                return {'error': 'Missing user ID.'}, 400

            user = Users.query.filter_by(id=user_id).first()

            if not user:
                return {'error': 'User not found!'}, 404

            db.session.delete(user)
            db.session.commit()

            page = request.args.get('page', 1, type=int)
            total_users = Users.query.count()
            max_page = (total_users - 1) // 10 + 1

            if page > max_page:
                page = max_page

            return {'success': 'User deleted successfully.', 'redirect': url_for('admin', page=page)}, 200

        except CSRFError:
            return {'error': 'CSRF token missing or invalid.'}, 403

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'An error occurred while deleting the user.'}, 500

        except Exception as e:
            return {'error': 'An unexpected error occurred.'}, 500
