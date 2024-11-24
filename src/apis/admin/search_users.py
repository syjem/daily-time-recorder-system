from flask import jsonify, request
from flask_restful import Resource
from sqlalchemy import or_
from sqlalchemy.orm import joinedload


from models.users import Users


class AdminUserSearch(Resource):

    def get(self):

        page = request.args.get('page', 1, type=int)
        per_page = 100

        name_query = request.args.get('name', '')

        if name_query:
            paginated_users = Users.query.filter(
                or_(
                    Users.first_name.like(f'%{name_query}%'),
                    Users.last_name.like(f'%{name_query}%')
                ),
                Users.role != 'admin'
            ).options(
                joinedload(Users.employment)
            ).paginate(
                page=page, per_page=per_page
            )

            data = [
                {
                    'id': user.id,
                    'avatar': user.avatar,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'employment_data': [
                        {
                            'id': emp.employee_id,
                            'company': emp.company,
                            'position': emp.position,
                            'hired_date': emp.hired_date
                        }
                        for emp in user.employment
                    ] if user.employment else None
                }
                for user in paginated_users.items
            ]

            start_index = (page - 1) * per_page + 1
            end_index = min(start_index + per_page - 1, paginated_users.total)

            return jsonify({
                'users': data,
                'pagination': {
                    'page': paginated_users.page,
                    'pages': paginated_users.pages,
                    'total': paginated_users.total,
                    'has_next': paginated_users.has_next,
                    'has_prev': paginated_users.has_prev,
                    'prev_num': paginated_users.prev_num,
                    'next_num': paginated_users.next_num,
                },
                'start_index': start_index,
                'end_index': end_index
            })
