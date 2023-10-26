from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField,SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired("This field is required")])
    password = PasswordField('Password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=10, message="The length must be greater than 3 and less than 10")
    ])
    remember = BooleanField('Remember')
    submit = SubmitField("Sign-in")


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Enter old password', validators=[DataRequired("This field is required!")])
    newpassword = PasswordField('Enter new password', validators=[
        DataRequired("This field is required"),
        Length(min=4, max=10, message="The length must be greater than 3 and less than 10")
    ])
    submit = SubmitField("Change password")
