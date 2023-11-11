from datetime import datetime

from flask import redirect, url_for, flash, session, request
from flask_login import login_required, current_user, login_user, logout_user

from app import app, db
from app.views import base_render
from app.forms.Login import LoginForm, ChangePasswordForm
from entitys.ToDo import ToDo
from app.forms.ToDo import ToDoForm

from entitys.User import AuthUser
from app.forms.User import RegistrationForm, ChangeUserDetailsForm


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
            change_user_details_form.old_password.errors.append("Old pass not valid")
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


@app.route('/todo', methods=["GET"])
@login_required
def todo_page():
    return base_render("todo-page.html", todo_list=ToDo.query.all(), todo_form=ToDoForm())


@app.route("/todo", methods=["POST"])
@login_required
def add_todo():
    todo_form = ToDoForm()
    if todo_form.validate_on_submit():
        new_todo = ToDo(title=todo_form.title.data, completed=False, status=ToDo.Status.IN_PROGRESS)
        db.session.add(new_todo)
        db.session.commit()

        flash('Todo added successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route("/todo/<string:id>")
@login_required
def delete_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route("/todo/<string:id>/update")
@login_required
def update_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    todo.complete()

    db.session.commit()
    flash('Todo updated successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route("/register", methods=["GET", "POST"])
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
        return redirect(url_for("login"))

    return base_render("sign_up.html", reg_form=reg_form)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("info"))

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
        return redirect(url_for("account"))

    return base_render("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    flash("You have successfully quit", "success")
    return redirect(url_for("login"))


@app.route("/change_password", methods=["POST"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        db_user = db.session.query(AuthUser).filter_by(email=current_user.email).first()

        if db_user and db_user.verify_password(form.old_password.data):
            db_user.password = form.new_password.data
            db.session.add(db_user)
            db.session.commit()
            flash("You have successfully changed your password", "success")
        else:
            form.old_password.errors.append("Enter the correct old password")

    return base_render("info.html", change_password_from=form, cookies=request.cookies.items())
