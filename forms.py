from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")

class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First name",
        validators=[DataRequired(), Length(max=100)]
    )
    last_name = StringField(
        "Surname",
        validators=[DataRequired(), Length(max=100)]
    )
    email = StringField(
        "Email address",
        validators=[DataRequired(), Email(), Length(max=255)]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)]
    )
    password2 = PasswordField(
        "Repeat password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )

    submit = SubmitField("Sign up")