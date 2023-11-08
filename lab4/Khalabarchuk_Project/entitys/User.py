from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp

from app import db, bcrypt, login_manager


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired("This field is required"),
        Length(4, 30, "The length must be greater than 4 and less than 30"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Nickname can include only letters, numbers, underscore and a dot')

    ])
    email = EmailField('Email(Login)', validators=[DataRequired("This field is required")])
    password = PasswordField('Password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=30, message="The length must be greater than 4 and less than 30")
    ])
    confirm_password = PasswordField('Confirm password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=30, message="The length must be greater than 4 and less than 30")
    ])
    submit = SubmitField("Sign-up")


class AuthUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(35), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), unique=False, nullable=False)
    avatar_image = db.Column(db.String(30), nullable=True, default="default.png")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password=password)

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def validate_username(username):
        if AuthUser.query.filter_by(username=username).first():
            raise ValidationError("Username is busy")

    @staticmethod
    def validate_email(email):
        if AuthUser.query.filter_by(email=email).first():
            raise ValidationError("Email is busy")

    @staticmethod
    @login_manager.user_loader
    def user_loader(user_id: int):
        return AuthUser.query.get(user_id)
