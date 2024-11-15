from datetime import datetime, timezone

from flask import Flask, make_response, render_template, redirect, request, session, url_for
from flask_cors import CORS
from flask_session import Session
from flask_migrate import Migrate
from flask_restful import Api
from flask_wtf import CSRFProtect
from sqlalchemy import event
from sqlalchemy.orm import joinedload
from sqlalchemy.engine import Engine

from config import Config
from models import db, Users, Passwords, Schedules, Tokens, Employment
from decorators import admin_required, login_required_and_get_user, redirect_to_dashboard
from helpers import ma, get_user_data, get_user_data_by_id, get_employment_data, handle_remember_me_token, format_datetime

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
Session(app)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)
ma.init_app(app)
csrf = CSRFProtect(app)


# Enable foreign key support in SQLite
@event.listens_for(Engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


from apis import AdminAddUser, AdminDeleteUser, SampleApi, ApiUserAvatar, PersonalInformation, EmploymentInformation  # noqa: E402


@app.before_request
def create_tables():
    db.create_all()


@app.before_request
def load_logged_in_user():
    if 'user_id' not in session:
        tkn = request.cookies.get('remember_token')

        if tkn:
            token_record = Tokens.query.filter_by(token=tkn).first()
            if token_record and token_record.expires_at.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc):
                session['user_id'] = str(token_record.user_id)


@app.context_processor
def inject_current_year():
    current_year = datetime.now().year
    return dict(current_year=current_year)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html"), 500


@app.route("/")
@redirect_to_dashboard
def index():
    return render_template("index.html")


@app.route("/sign-in", methods=['GET', 'POST'])
@redirect_to_dashboard
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = 'remember_me' in request.form

        if not email or not password:
            error = "Please, enter your email and password."
            return render_template("login.html", error=error)

        user = Users.query.filter_by(email=email).first()

        if user:
            user_password = Passwords.query.filter_by(user_id=user.id).first()

            if user_password and user_password.check_password(password):
                session['user_id'] = str(user.id)

                if remember_me:
                    response = handle_remember_me_token(user)
                    return response

                print(f'USER ROLE: {user.role}')

                if user.role != 'admin':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('admin'))

            else:
                password_error = 'You entered an incorrect password.'
                return render_template("login.html", email=email, password_error=password_error)

        else:
            email_error = 'Email not found.'
            return render_template("login.html", email_error=email_error)

    return render_template("login.html")


@app.route("/logout")
@login_required_and_get_user
def logout(user):
    Tokens.query.filter_by(user_id=user.id).delete()
    db.session.commit()

    session.clear()
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('remember_token')
    return response


@app.route("/attendance")
@login_required_and_get_user
def dashboard(user):

    first_name, last_name, email, _, _, image = get_user_data(user)
    formatted_date = format_datetime(datetime.now())

    return render_template(
        "dashboard.html",
        first_name=first_name,
        last_name=last_name,
        email=email,
        avatar=image,
        date=formatted_date
    )


@app.route('/time-schedule', methods=['GET', 'POST'])
@login_required_and_get_user
def time_schedule(user):

    first_name, last_name, email, _, _, image = get_user_data(user)
    schedules = Schedules.query.filter_by(
        user_id=user.id).order_by(Schedules.id).all()

    data = [{
            'day': schedule.day,
            'shift_type': (
                'Day off' if schedule.day_off == True else schedule.shift_type
            ),
            'schedule': (
                '6:00 AM - 3:00 PM' if schedule.shift_type == 'Opener' else
                '8:30 AM - 5:30 PM' if schedule.shift_type == 'Regular' else
                '1:00 PM - 10:00 PM' if schedule.shift_type == 'Closer' else ''
            )
            } for schedule in schedules]

    headers = ['Day', 'Shift', 'Schedule']

    return render_template(
        "time-schedule.html",
        first_name=first_name,
        last_name=last_name,
        email=email,
        avatar=image,
        schedules=data,
        headers=headers
    )


@app.route('/daily-logs', methods=['GET', 'POST'])
@login_required_and_get_user
def daily_logs(user):

    first_name, last_name, email, _, _, image = get_user_data(user)

    return render_template(
        "daily-logs.html",
        first_name=first_name,
        last_name=last_name,
        email=email,
        avatar=image
    )


@app.route('/profile')
@login_required_and_get_user
def profile(user, user_id=None):

    return redirect(url_for('user_profile', user_id=user.id))


@app.route('/user/<string:user_id>', methods=['GET', 'POST'])
@login_required_and_get_user
def user_profile(user, user_id):

    first_name, last_name, email, birthday, _, image = get_user_data(user)
    # employee_id, company, hired_date, position = get_employment_data(user)

    return render_template(
        "user-profile.html",
        first_name=first_name,
        last_name=last_name,
        email=email,
        birthday=birthday,
        avatar=image
    )


@app.route('/admin/')
@admin_required
def admin(user):
    first_name, last_name, email, _, _, image = get_user_data(user)

    page = request.args.get('page', 1, type=int)
    per_page = 10

    paginated_users = Users.query.filter(Users.role != 'admin').options(
        joinedload(Users.employment)).paginate(page=page, per_page=per_page)

    user_employment_data = {
        user.id: user.employment for user in paginated_users.items}

    # Calculate start and end index for displayed users
    start_index = (page - 1) * per_page + 1
    end_index = min(start_index + per_page - 1, paginated_users.total)

    table_columns = ['Name', 'Company', 'Position', 'Actions']

    return render_template(
        'admin/admin.html',
        first_name=first_name,
        last_name=last_name,
        email=email,
        avatar=image,
        users=paginated_users,
        employment_data=user_employment_data,
        table_columns=table_columns,
        start_index=start_index,
        end_index=end_index
    )


@app.route('/admin/user/<string:user_id>/edit')
@admin_required
def admin_user_edit(user, user_id):
    first_name, last_name, email, birthday, role, image = get_user_data_by_id(
        user_id)

    return render_template(
        'user-profile.html',
        first_name=first_name,
        last_name=last_name,
        email=email,
        birthday=birthday,
        role=role,
        avatar=image
    )


api.add_resource(SampleApi, '/api/sample')
api.add_resource(ApiUserAvatar, '/api/user/avatar')
api.add_resource(PersonalInformation, '/api/user/personal_info')
api.add_resource(EmploymentInformation, '/api/user/employment_information')


api.add_resource(AdminAddUser, '/api/admin/user/add')
api.add_resource(AdminDeleteUser, '/api/admin/user/<string:user_id>/delete')
