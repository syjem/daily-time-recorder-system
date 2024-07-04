from flask import flash, Flask, jsonify, make_response, render_template, redirect, request, session, url_for
from flask_cors import CORS
from flask_session import Session
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_restful import Api


from config import Config
from models import db, Users
from decorators import login_required, login_required_and_get_user, logout_required, redirect_to_dashboard, redirect_to_profile_page
from helpers import generate_confirmation_code, get_user_data, save_profile_upload
from apis import Sample_Api, Upload_User_Profile

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
Session(app)

db.init_app(app)
mail = Mail(app)
migrate = Migrate(app, db)
api = Api(app)


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

        # Check if email already exists
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
        flash("Check your email", 'success')
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
            return render_template("confirm-email.html", error=error)

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


@app.route("/profile-setup", methods=['GET', 'POST'])
@login_required
@redirect_to_profile_page
def profile_setup(user):
    error = ''

    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        email = session.get('email')
        file = request.files.get('profile-picture')

        # Validate form data
        if not name or not password:
            error = "All fields are required."
            return render_template('profile-setup.html', error=error)

        if file and file.filename != '':
            filepath = save_profile_upload(file)
        else:
            filepath = None

        user = Users.query.filter_by(email=email).first()
        user.name = name
        user.set_password(password)
        if filepath:
            user.image_file = filepath

        db.session.commit()
        flash("Profile setup successful.", 'success')
        return redirect(url_for('dashboard'))

    return render_template("profile-setup.html")


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


@app.route("/dashboard")
@login_required_and_get_user
def dashboard(user):

    name, email, image = get_user_data(user)

    return render_template("dashboard.html", name=name, email=email, image_src=image)


@app.route('/time-schedule', methods=['GET', 'POST'])
@login_required_and_get_user
def time_schedule(user):

    name, email, image = get_user_data(user)

    return render_template("time-schedule.html", name=name, email=email, image_src=image)


@app.route('/daily-logs', methods=['GET', 'POST'])
@login_required_and_get_user
def daily_logs(user):

    name, email, image = get_user_data(user)

    return render_template("daily-logs.html", name=name, email=email, image_src=image)


@app.route('/profile')
@login_required_and_get_user
def profile(user, user_id=None):

    return redirect(url_for('user_profile', user_id=user.id))


@app.route('/user/<string:user_id>', methods=['GET', 'POST'])
@login_required_and_get_user
def user_profile(user, user_id):

    name, email, image = get_user_data(user)

    return render_template("user-profile.html", name=name, email=email, image_src=image)


@app.route("/forgot-password", methods=['GET', 'POST'])
@logout_required
def forgot_password():
    return render_template("forgot-password.html")


@app.route("/reset-password", methods=['GET', 'POST'])
@login_required
def reset_password():
    return render_template("reset-password.html")


@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template("terms-and-conditions.html")


api.add_resource(Sample_Api, '/api/sample')
api.add_resource(Upload_User_Profile, '/api/upload/user/profile')


if __name__ == '__main__':
    app.run(debug=True)
