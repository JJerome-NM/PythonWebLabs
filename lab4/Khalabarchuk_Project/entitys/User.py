from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email

from app import db, bcrypt


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired("This field is required")])
    email = EmailField('Email(Login)', validators=[DataRequired("This field is required")])
    password = PasswordField('Password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=30, message="The length must be greater than 3 and less than 30")
    ])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=30, message="The length must be greater than 3 and less than 30")
    ])
    submit = SubmitField("Sign-up")


class AuthUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), unique=False, nullable=False)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password=password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class User:

    def __init__(self, login: str, password: str):
        self.login = str(login)
        self.password = password

    def __eq__(self, other):
        if isinstance(other, User):
            return self.login == other.login and self.password == other.password
        return False

    def __hash__(self):
        return hash((self.login, self.password))
