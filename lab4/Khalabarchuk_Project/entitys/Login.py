from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Length


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
