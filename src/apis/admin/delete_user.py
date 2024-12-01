
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

            # name = request.args.get('name')
            page = request.args.get('page', type=int)
            total_users = Users.query.count()
            max_page = (total_users - 1) // 10 + 1

            redirect_url = ''

            if page:
                if page > max_page:
                    page = max_page
                    redirect_url = url_for('admin_manage_users', page=page)
            # else:
            #     redirect_url = url_for('admin_manage_users')

            # if name:
            #     redirect_url = url_for('admin_manage_users')

            return {
                'success': 'User deleted successfully.',
                'redirect': redirect_url
            }, 200

        except CSRFError:
            return {'error': 'CSRF token missing or invalid.'}, 403

        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': 'An error occurred while deleting the user.'}, 500

        except Exception as e:
            return {'error': 'An unexpected error occurred.'}, 500
