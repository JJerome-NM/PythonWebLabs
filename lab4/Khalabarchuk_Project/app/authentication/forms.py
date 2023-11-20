from flask_login import current_user
from flask_wtf.file import FileAllowed, FileField
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp, ValidationError

from .entitys import AuthUser


class UserRegistrationBaseImplementationForm(FlaskForm):

    def validate_username(self, username):
        if current_user.is_authenticated and current_user.username == username.data:
            return

        if AuthUser.query.filter_by(username=username.data).first():
            raise ValidationError("Username is busy")

    def validate_email(self, email):
        if current_user.is_authenticated and current_user.email == email.data:
            return

        if AuthUser.query.filter_by(email=email.data).first():
            raise ValidationError("Email is busy")


class RegistrationForm(UserRegistrationBaseImplementationForm, FlaskForm):
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


class ChangeUserDetailsForm(UserRegistrationBaseImplementationForm, FlaskForm):
    username = StringField('Username', validators=[
        DataRequired("This field is required"),
        Length(4, 30, "The length must be greater than 4 and less than 30"),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Nickname can include only letters, numbers, underscore and a dot')
    ])
    email = EmailField('Email(Login)', validators=[DataRequired("This field is required")])
    avatar_image = FileField("User avatar", validators=[
        FileAllowed(["jpg", "png", "jfif", "gif"])
    ])
    about_me = TextAreaField(label="About me:", validators=[
        Length(min=0, max=500, message="The length must be less than 500 chars")
    ])
    new_password = PasswordField('New password', validators=[])
    confirm_password = PasswordField('Confirm new password', validators=[])
    old_password = PasswordField('Current password', validators=[
        DataRequired("To save changes, you need to enter the old password")
    ])
    submit = SubmitField("Save changes")

    def validate_new_password(self, password):
        if password.data and 4 > len(password.data) < 30:
            raise ValidationError("The length must be greater than 4 and less than 30")

    def validate_confirm_password(self, password):
        if password.data and 4 > len(password.data) < 30:
            raise ValidationError("The length must be greater than 4 and less than 30")

        if self.new_password.data and password.data != self.new_password.data:
            raise ValidationError("New password must be the identical to confirm password")

    def validate_old_password(self, old_pass):
        if old_pass.data and not current_user.verify_password(old_pass.data):
            raise ValidationError("The password you entered is not correct")

class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired("This field is required")])
    password = PasswordField('Password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=30, message="The length must be greater than 3 and less than 30")
    ])
    remember = BooleanField('Remember')
    submit = SubmitField("Sign-in")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired("This field is required!")])
    new_password = PasswordField('New password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=10, message="The length must be greater than 3 and less than 10")
    ])
    submit = SubmitField("Change password")

