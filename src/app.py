from flask import flash, Flask, make_response, render_template, redirect, request, session, url_for
from flask_cors import CORS
from flask_session import Session
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from models import db, Users
from decorators import login_required, login_required_and_get_user, logout_required, redirect_to_dashboard, redirect_to_profile_page
from helpers import ma, generate_confirmation_code, get_user_data

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
Session(app)

db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)
api = Api(app)
ma.init_app(app)


from apis import SampleApi, ApiUserAvatar, SetupUserProfile, PersonalInformation, EmploymentInformation  # noqa: E402


@app.route('/sample')
def sample():
    return render_template('sample.html')


@app.before_request
def create_tables():
    db.create_all()


@app.before_request
def load_logged_in_user():
    if 'user_id' not in session:
        token = request.cookies.get('remember_token')

        if token:
            user = Users.query.filter_by(remember_token=token).first()
            if user:
                session['user_id'] = str(user.id)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route("/")
@redirect_to_dashboard
def index():
    return render_template("index.html")


@app.route("/sign-up", methods=['GET', 'POST'])
@logout_required
def sign_up():
    error = ''

    if request.method == 'POST':
        email = request.form.get("email")

        if not email:
            error = "Email field is required."
            return render_template("sign-up.html", error=error)

        if Users.query.filter_by(email=email).first():
            flash("Sorry, email is already in use.", 'danger')
            return redirect(url_for('sign_up'))

        code = generate_confirmation_code(64)

        # Store the confirmation code in the session
        session["confirmation_code"] = code
        session["email"] = email

        # Send confirmation code via email
        msg = Message("Email Confirmation", recipients=[
                      email], body=f"Your confirmation code is: {code}")
        mail.send(msg)
        flash("Sent, check your email", 'success')
        return redirect(url_for('confirm_email'))

    return render_template("sign-up.html")


@app.route("/confirm-email", methods=["GET", "POST"])
@logout_required
def confirm_email():
    error = ''

    if request.method == "POST":
        confirmation_code = request.form.get('confirmation-code')

        if not confirmation_code:
            error = "Confirmation code is required."
            return redirect(url_for('confirm_email'), error=error)

        # Check if the confirmation code matches
        if confirmation_code == session.get("confirmation_code"):
            session.pop('confirmation_code', None)
            email = session.get('email')

            # Create user with email
            user = Users(email=email)
            db.session.add(user)
            db.session.commit()

            # Store user ID in session
            session['user_id'] = str(user.id)

            flash("Email confirmed", 'success')
            return redirect(url_for('profile_setup'))
        else:
            error = "Invalid confirmation code."
            return render_template("confirm-email.html", error=error)

    return render_template("confirm-email.html")


@app.route("/profile-setup")
@login_required
@redirect_to_profile_page
def profile_setup(user):
    if user.image_file:
        image_src = url_for(
            'static', filename=f'assets/upload/users/{user.image_file}')
    else:
        image_src = url_for('static', filename=f'assets/avatar.png')

    return render_template("profile-setup.html", image_src=image_src)


@app.route("/sign-in", methods=['GET', 'POST'])
@logout_required
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = 'remember_me' in request.form

        if not email or not password:
            flash("Email and password are required", 'danger')
            return redirect(url_for('sign_in'))

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = str(user.id)

            if remember_me:
                token = user.generate_remember_token()
                db.session.commit()

                response = make_response(redirect(url_for('dashboard')))
                response.set_cookie('remember_token', token,
                                    max_age=30*24*60*60)
                return response

            return redirect(url_for('dashboard'))

        else:
            flash('Invalid credentials.', 'danger')
            return redirect(url_for('sign_in'))

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('remember_token')
    return response


@app.route("/attendance")
@login_required_and_get_user
def dashboard(user):

    first_name, last_name, employee_id, email, _, position, image = get_user_data(
        user)

    return render_template("dashboard.html", first_name=first_name, last_name=last_name, employee_id=employee_id, email=email, position=position, image_src=image)


@app.route('/time-schedule', methods=['GET', 'POST'])
@login_required_and_get_user
def time_schedule(user):

    first_name, last_name, employee_id, email, _, position, image = get_user_data(
        user)

    return render_template("time-schedule.html", first_name=first_name, last_name=last_name, employee_id=employee_id, email=email, position=position, image_src=image)


@app.route('/daily-logs', methods=['GET', 'POST'])
@login_required_and_get_user
def daily_logs(user):

    first_name, last_name, employee_id, email, _, position, image = get_user_data(
        user)

    return render_template("daily-logs.html", first_name=first_name, last_name=last_name, employee_id=employee_id, email=email, position=position, image_src=image)


@app.route('/profile')
@login_required_and_get_user
def profile(user, user_id=None):

    return redirect(url_for('user_profile', user_id=user.id))


@app.route('/user/<string:user_id>', methods=['GET', 'POST'])
@login_required_and_get_user
def user_profile(user, user_id):

    first_name, last_name, employee_id, email, birthday, position, image = get_user_data(
        user)

    return render_template("user-profile.html", first_name=first_name, last_name=last_name, employee_id=employee_id, email=email, birthday=birthday, position=position, image_src=image)


@app.route("/forgot-password", methods=['GET', 'POST'])
@logout_required
def forgot_password():
    return render_template("forgot-password.html")


@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template("terms-and-conditions.html")


api.add_resource(SampleApi, '/api/sample')
api.add_resource(ApiUserAvatar, '/api/user/avatar')
api.add_resource(SetupUserProfile, '/api/profile_setup')
api.add_resource(PersonalInformation, '/api/user/personal_info')
api.add_resource(EmploymentInformation, '/api/user/employment_information')

if __name__ == '__main__':
    app.run(debug=True)
