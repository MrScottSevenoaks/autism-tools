from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_login import LoginManager
from flask_wtf import CSRFProtect


app = Flask(__name__)


# --- Config ---
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///autism_app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)  # enable CSRF protection

login_manager = LoginManager(app)
login_manager.login_view = "login"  # where to redirect for @login_required
login_manager.login_message = "You need to sign in before using the tools."
login_manager.login_message_category = "info"  # or "warning", "danger", etc.

# --- Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# --- Routes ---

from forms import RegistrationForm, LoginForm

@app.route("/")
def index():
    """
    Landing page: explains Word Board + Food Tracking tool
    and shows the login form (index.html extends base.html).
    """
    form = LoginForm()
    return render_template("index.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=form.remember_me.data)
            flash("Logged in successfully.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "danger")

    # Either show dedicated login page, or reuse index.html
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        email = form.email.data.strip().lower()

        existing = User.query.filter_by(email=email).first()
        if existing:
            form.email.errors.append("An account with that email already exists.")
            # fall through to render_template with error
        else:
            user = User(
                email=email,
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            flash("Account created. You can now log in.", "success")
            return redirect(url_for("login"))

    # On GET or failed validation
    return render_template("register.html", form=form)

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    """
    Placeholder for:
      <a href="{{ url_for('forgot_password') }}" class="small">
    """
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        # Here you’d generate a reset token and send an email.
        # For now we just pretend to.
        if email:
            flash(
                "If that email exists in our system, a reset link has been sent.",
                "info",
            )
        return redirect(url_for("forgot_password"))

    return render_template("forgot_password.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Example protected page after login.
    Here you’d link to:
      - Word Board
      - Food Tracking Tool
    """
    return render_template("dashboard.html")


@app.route("/word-board")
@login_required
def word_board():
    items = [
        {"word": "Drink", "icon": "🥤"},
        {"word": "Hungry", "icon": "🍗"},
        {"word": "Toilet", "icon": "🚽"},
        {"word": "Help", "icon": "🆘"},
        {"word": "More", "icon": "➕"},
        {"word": "Stop", "icon": "🛑"},
        {"word": "Yes", "icon": "✅"},
        {"word": "No", "icon": "❌"},
    ]
    return render_template("word_board.html", items=items)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))


# --- CLI helper for first run ---
@app.cli.command("init-db")
def init_db():
    """Initialise the database: flask init-db"""
    db.create_all()
    print("Database initialised.")


if __name__ == "__main__":
    app.run(
        debug=True,        # turn on debug mode
        host="0.0.0.0",    # needed for Codespaces
        port=5000
    )