from datetime import datetime

from flask import flash
from flask_login import login_required, current_user

from app import db
from ..authentication.entitys import AuthUser
from ..common_logic import base_render
from .forms import ChangeUserDetailsForm

from . import user_bp as app


@app.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.now().replace(microsecond=0)
        try:
            db.session.commit()
        except:
            flash('Error while update user last seen!', 'danger')
    return response


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    change_user_details_form = ChangeUserDetailsForm()

    if change_user_details_form.validate_on_submit():

        if not current_user.verify_password(change_user_details_form.old_password.data):
            change_user_details_form.old_password.errors.append("The password you entered is not correct")
            return base_render("account.html", form=change_user_details_form)

        if change_user_details_form.avatar_image.data:
            current_user.set_avatar_image(change_user_details_form.avatar_image.data)

        current_user.username = change_user_details_form.username.data
        current_user.email = change_user_details_form.email.data
        current_user.about_me = change_user_details_form.about_me.data

        if change_user_details_form.new_password.data:
            current_user.password = change_user_details_form.new_password.data

        db.session.commit()

        flash('Your account information has been successfully updated', 'success')

    else:
        change_user_details_form.username.data = current_user.username
        change_user_details_form.email.data = current_user.email
        change_user_details_form.about_me.data = current_user.about_me

    return base_render("account.html", form=change_user_details_form)


@app.route("/users")
@login_required
def get_users():
    return base_render("all-users.html", users=AuthUser.query.all())
