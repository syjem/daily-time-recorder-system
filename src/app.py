from flask import flash, Flask, render_template, redirect, request, session, url_for
from flask_cors import CORS
# from flask_session import Session
from flask_mail import Mail, Message


from config import Config
from models import db
from helpers import dashboard_redirect, email_session_required, generate_confirmation_code, login_required, logout_required

app = Flask(__name__)
CORS(app)
# Session(app)

app.config.from_object(Config)
mail = Mail(app)
db.init_app(app)

# with app.app_context():
#     db.create_all()


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

        code = generate_confirmation_code(64)

        # Store the confirmation code in the session
        session["confirmation_code"] = code
        session["email"] = email

        # Send confirmation code via email
        msg = Message("Email Confirmation", recipients=[
                      email], body=f"Your confirmation code is: {code}")
        mail.send(msg)
        flash(
            f"Email confirmation was successfully sent", 'green')
        return redirect(url_for('confirm_email'))

    return render_template("sign-up.html")


@app.route("/confirm-email", methods=["GET", "POST"])
@logout_required
def confirm_email():
    if request.method == "POST":
        confirmation_code = request.form.get('confirmation-code')

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
    return render_template("profile-setup.html")


@app.route("/sign-in", methods=['GET', 'POST'])
@logout_required
def sign_in():
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
    redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.run(debug=True)
