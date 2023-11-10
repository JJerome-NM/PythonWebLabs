from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

from entitys.User import AuthUser

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

    def validate_username(self, username):
        if AuthUser.query.filter_by(username=username.data).first():
            raise ValidationError("Username is busy")

    def validate_email(self, email):
        if AuthUser.query.filter_by(email=email.data).first():
            raise ValidationError("Email is busy")
