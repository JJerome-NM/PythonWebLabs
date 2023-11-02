import datetime
import json
import platform

from flask import render_template, request, session, redirect, url_for, make_response, flash

from app import app
from app import db
from entitys.LoginForm import LoginForm, ChangePasswordForm
from entitys.ToDo import ToDo, ToDoForm
from entitys.Comment import CommentForm, Comment

PROJECTS_LIST = [{
    "photo_url": "projectNMWS.png",
    "name": "NM-WebSockets",
    "project_url": "https://github.com/JJerome-NM/NM-WebSockets"
}, {
    "photo_url": "projectCodenames.png",
    "name": "CodeNames",
    "project_url": "https://github.com/JJerome-NM/CodeNames"
}, {
    "photo_url": "projectWSHelper.png",
    "name": "WebSocketHelper",
    "project_url": "https://github.com/JJerome-NM/WebSocketHelper"
}]

CONTACTS = [{
    "type": "EMAIL",
    "contact_name": "Gmail",
    "name": "Mykhailo Khalabarchuk",
    "link": "mykhailo.khalabarchuk.21@pnu.edu.ua",
    "title": "JJerome-NM"
}, {
    "type": "DEFAULT",
    "contact_name": "Linkedin",
    "name": "Mykhailo Khalabarchuk",
    "link": "https://www.linkedin.com/in/mykhailo-khalabarchuk-26376528b/",
    "title": "Mykhailo Khalabarchuk"
}, {
    "type": "DEFAULT",
    "contact_name": "Github",
    "name": "Михайло Халабарчук",
    "link": "https://github.com/JJerome-NM",
    "title": "Михайло Халабарчук"
}]

SKILLS_LIST = list([{
    "name": "Java Core",
    "title": "Java Core, often referred to as 'Core Java,' is a term used to describe the fundamental and essential components of the Java programming language. It encompasses the basic concepts, libraries, and features that are integral to Java development. Core Java forms the foundation upon which more advanced Java technologies and frameworks are built.",
}, {
    "name": "Java Spring",
    "title": "Java Spring, often referred to simply as Spring, is a popular and powerful framework for building Java-based enterprise applications. It provides a comprehensive infrastructure for developing robust and maintainable applications, with a focus on modularity, scalability, and ease of testing. Spring is known for simplifying many aspects of Java development and has become a cornerstone of the Java ecosystem for building web, cloud, and enterprise applications.",
}, {
    "name": "Spring Data",
    "title": "Spring Data is a part of the larger Spring Framework ecosystem that simplifies data access and persistence in Java applications. It provides a unified and consistent way to interact with various data sources, such as relational databases, NoSQL databases, and other data storage technologies. Spring Data aims to reduce the boilerplate code typically required for data access and to improve developer productivity.",
}, {
    "name": "Spring Security",
    "title": "Spring Security is a powerful and highly customizable security framework provided by the Spring Framework for building secure Java-based applications. It focuses on authentication, authorization, and protection against common security vulnerabilities. Spring Security is widely used in web applications, microservices, and other Java-based systems to ensure the security of the application and its resources.",
}, {
    "name": "Python",
    "title": "Python is a high-level, versatile, and interpreted programming language that has gained tremendous popularity in the world of computer programming since its creation in the late 1980s. Here are some key aspects of Python as a skill:",
}, {
    "name": "WebSocket",
    "title": "WebSocket is a communication protocol that provides full-duplex, bidirectional communication channels over a single TCP connection. It is designed to be efficient and lightweight, making it a suitable choice for real-time web applications. WebSocket allows for interactive and dynamic communication between a client (usually a web browser) and a server, enabling data to be transmitted in both directions without the need for the client to repeatedly request data",
}, {
    "name": "Rest",
    "title": "Rest is a fundamental skill that is crucial for maintaining physical and mental well-being. It refers to the act of taking a break or allowing oneself to relax and recuperate from physical, mental, or emotional exertion. Rest is essential for recharging and revitalizing the body and mind. Here are some key aspects of the skill of rest",
}])


def base_render(template: str, **context):
    return render_template(template, about_os=platform.platform(), user_agent_info=request.user_agent.string, **context)


def secured_render(template: str, **context):
    if session.get("user_data") is None:
        return redirect(url_for("login"))
    return base_render(template, **context)


@app.route("/comments")
def comments_page():
    return secured_render("comments-page.html", comment_form=CommentForm(), comments=Comment.query.all())


@app.route("/comments", methods=["POST"])
def add_comment():
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        user_login = session["user_data"].get("login")
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_comment = Comment(username=user_login, comment=comment_form.comment.data, date=date)
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added successfully', 'success')
    else:
        flash('Something went wrong while adding a comment', 'danger')

    return redirect(url_for("comments_page"))


@app.route('/todo', methods=["GET"])
def todo_page():
    return secured_render("todo-page.html", todo_list=ToDo.query.all(), todo_form=ToDoForm())


@app.route("/todo", methods=["POST"])
def add_todo():
    todo_form = ToDoForm()
    if todo_form.validate_on_submit():
        new_todo = ToDo(title=todo_form.title.data, completed=False, status=ToDo.Status.IN_PROGRESS)
        db.session.add(new_todo)
        db.session.commit()

        flash('Todo added successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route("/todo/<string:id>")
def delete_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route("/todo/<string:id>/update")
def update_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    todo.complete()

    db.session.commit()
    flash('Todo updated successfully', 'success')

    return redirect(url_for("todo_page"))


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        with open("users.json", "r") as users_data:
            users = json.load(users_data)

            if form.login.data in users \
                    and form.password.data == users[form.login.data]["password"] \
                    and form.remember.data:
                session["user_data"] = users[form.login.data]["data"]
                session["user_data"]["login"] = form.login.data

                flash("You have successfully signed-in", "success")
                return redirect(url_for("info"))
            else:
                flash("You are logged in without remembering", "success")
                return base_render("info.html", cookies=request.cookies.items())

        flash("Check the privilege of entering your login and password", "danger")

    return base_render("login.html", form=form)


@app.route("/logout")
def logout():
    session.clear()
    flash("You have successfully quit", "success")
    return redirect(url_for("login"))


@app.route("/change_password", methods=["POST"])
def change_password():
    user_login = session["user_data"].get("login")

    form = ChangePasswordForm()

    if form.validate_on_submit():
        with open("users.json", "r") as file:
            users = json.load(file)

            if form.old_password.data == users[user_login]["password"]:
                users[user_login]["password"] = form.new_password.data
            else:
                flash("Enter the correct old password", "danger")
                return redirect(url_for("info"))

        with open("users.json", "w") as file:
            json.dump(users, file)
            flash("You have successfully changed your password", "success")

    return secured_render("info.html", change_password_from=form, cookies=request.cookies.items())


@app.route("/info")
def info():
    form = ChangePasswordForm()
    return secured_render("info.html", change_password_from=form, cookies=request.cookies.items())


@app.route("/add_cookie", methods=["POST"])
def add_cookie():
    cookie_key = request.form.get("cookie_key")
    cookie_value = request.form.get("cookie_value")
    cookie_exp = request.form.get("expires_at")

    response = make_response(redirect(url_for("info")))
    response.set_cookie(cookie_key, cookie_value, expires=cookie_exp)

    flash("You added a fancy cookie", "info")
    return response


@app.route("/remove_cookie", methods=["POST"])
def remove_cookie():
    cookie_key = request.form.get("cookie_key")

    response = make_response(redirect(url_for("info")))

    if cookie_key is None:
        for key in request.cookies.keys():
            if key != "session":
                response.delete_cookie(key)

        flash("You have given all the cookies", "info")
        return response

    if cookie_key not in request.cookies.keys():
        flash(f"Undefined {cookie_key}", "danger")
        return redirect(url_for('info'))

    response.delete_cookie(cookie_key)
    flash(f"Unfortunately, we have successfully deleted your cookie {cookie_key}", "warning")
    return response


@app.route('/')
@app.route('/portfolio')
def portfolio_main():
    return base_render("portfolio-main.html")


@app.route('/projects')
def portfolio_projects():
    return base_render("portfolio-projects.html", projects_list=PROJECTS_LIST)


@app.route('/contacts')
def portfolio_contacts():
    return base_render("portfolio-contacts.html", contacts=CONTACTS)


@app.route('/skills')
@app.route('/skills/<int:id>')
def portfolio_skills(id: int = None):
    if id is not None:
        return base_render("portfolio-skills.html", selected_skill=SKILLS_LIST[id])

    return base_render("portfolio-skills.html", all_skills_list=SKILLS_LIST)
