import uuid
from flask import flash, Flask, render_template, redirect, request, session, url_for
from flask_cors import CORS
from flask_session import Session
from flask_mail import Mail, Message


from config import Config
from models import db, Users
from decorators import dashboard_redirect, email_session_required, login_required, logout_required
from helpers import generate_confirmation_code

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
Session(app)

mail = Mail(app)
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
@dashboard_redirect
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.route('/terms-and-conditions')
def terms_and_conditions():
    return render_template("terms-and-conditions.html")


@app.route("/sign-up", methods=['GET', 'POST'])
@logout_required
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")

        if not email:
            return "Email field is required."

        # Check if email already exists
        if Users.query.filter_by(email=email).first():
            flash("Sorry, email is already in use.", 'red')
            return redirect(url_for('sign_up'))

        code = generate_confirmation_code(64)

        # Store the confirmation code in the session
        session["confirmation_code"] = code
        session["email"] = email

        # Send confirmation code via email
        msg = Message("Email Confirmation", recipients=[
                      email], body=f"Your confirmation code is: {code}")
        mail.send(msg)
        flash(
            "Email confirmation was successfully sent", 'green')
        return redirect(url_for('confirm_email'))

    return render_template("sign-up.html")


@app.route("/confirm-email", methods=["GET", "POST"])
@logout_required
def confirm_email():
    if request.method == "POST":
        confirmation_code = request.form.get('confirmation-code')

        if not confirmation_code:
            flash("Please enter the confirmation code.", 'red')
            return redirect(url_for('confirm_email'))

        # Check if the confirmation code matches
        if confirmation_code == session.get("confirmation_code"):
            session.pop('confirmation_code', None)
            flash("Email confirmed", 'green')
            return redirect(url_for('profile_setup'))
        else:
            flash("Invalid confirmation code.", 'red')
            return redirect(url_for('confirm_email'))

    return render_template("confirm-email.html")


@app.route("/profile-setup", methods=['GET', 'POST'])
@logout_required
@email_session_required
def profile_setup():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        password = request.form.get('password')
        email = session.get('email')

        # Validate form data
        if not first_name or not last_name or not password:
            flash("All fields are required.", 'red')
            return redirect(url_for('profile_setup'))

        user = Users(first_name=first_name, last_name=last_name,
                     email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = str(user.id)
        print(f"Session ID: {session.get('user_id')}")
        flash("Profile setup successful.", 'green')
        return redirect(url_for('dashboard'))

    return render_template("profile-setup.html")


@app.route("/sign-in", methods=['GET', 'POST'])
@logout_required
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email and not password:
            flash('All fields are required.', 'red')
            return redirect(url_for('sign_in'))

        user = Users.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = str(user.id)
            return redirect(url_for('dashboard'))

        else:
            flash('Invalid email or password.', 'red')
            return redirect(url_for('sign_in'))

    return render_template("login.html")


@app.route("/forgot-password", methods=['GET', 'POST'])
@logout_required
def forgot_password():
    return render_template("forgot-password.html")


@app.route("/reset-password", methods=['GET', 'POST'])
@login_required
def reset_password():
    return render_template("reset-password.html")


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session.get('user_id')

    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        flash('Invalid user ID.', 'red')
        return redirect(url_for('sign_in'))

    user = Users.query.filter_by(id=user_uuid).first()

    if not user:
        flash('User not found.', 'red')
        return redirect(url_for('sign_in'))

    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    return render_template("dashboard.html", first_name=first_name, last_name=last_name, email=email)


@app.route('/time-schedule', methods=['GET', 'POST'])
@login_required
def time_schedule():
    return render_template("time-schedule.html")


@app.route('/daily-logs', methods=['GET', 'POST'])
@login_required
def daily_logs():
    return render_template("daily-logs.html")


@app.route('/profile/<string:user_id>', methods=['GET', 'POST'])
@login_required
def user_profile(user_id):
    return render_template("user-profile.html")


if __name__ == '__main__':
    app.run(debug=True)
