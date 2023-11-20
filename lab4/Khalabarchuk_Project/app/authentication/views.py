from flask import redirect, url_for, flash, session, request
from flask_login import login_required, current_user, login_user, logout_user

from ..common_logic import base_render
from .. import db

from .forms import LoginForm, ChangePasswordForm, RegistrationForm, ChangeUserDetailsForm
from ..authentication.entitys import AuthUser

from . import auth_bp


@auth_bp.route("/users")
@login_required
def get_users():
    return base_render("all-users.html", users=AuthUser.query.all())


@auth_bp.route("/register", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("info"))

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        user = AuthUser(email=reg_form.email.data, username=reg_form.username.data,
                        password=reg_form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('You have successfully registered', 'success')
        return redirect(url_for("auth.login"))

    return base_render("sign_up.html", reg_form=reg_form)


@auth_bp.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("common.info"))

    form = LoginForm()

    if form.validate_on_submit():
        db_user = db.session.query(AuthUser).filter_by(email=form.login.data).first()

        if not db_user or not db_user.verify_password(password=form.password.data):
            form.login.errors.append("Login or password is incorrect")
            form.password.errors.append("Login or password is incorrect")
            flash("Login or password is incorrect", 'danger')
            return base_render("login.html", form=form)

        login_user(db_user, remember=form.remember.data)

        flash("You have successfully signed-in", "success")
        return redirect(url_for("user.account"))

    return base_render("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    flash("You have successfully quit", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/change_password", methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        db_user = db.session.query(AuthUser).filter_by(email=current_user.email).first()

        if db_user and db_user.verify_password(form.old_password.data):
            db_user.password = form.new_password.data
            db.session.add(db_user)
            db.session.commit()
        else:
            flash("You have successfully changed your password", "success")
            form.old_password.errors.append("Enter the correct old password")

    return base_render("info.html", change_password_from=form, cookies=request.cookies.items())
