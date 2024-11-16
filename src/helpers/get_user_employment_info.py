from models.employments import Employment


def get_employment_data(user):
    user = Employment.query.filter_by(user_id=user.id).first()
    if user:
        employee_id = user.employee_id
        company = user.company
        hired_date = user.hired_date
        position = user.position

        return employee_id, company, hired_date, position

    return '', '', '', ''
