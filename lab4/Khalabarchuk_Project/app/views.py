import json
import platform

from flask import render_template, request, session, redirect, url_for, make_response

from entitys.User import User
from app import app


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


def render_template_with_base_template(template: str, **context):
    return render_template(template, about_os=platform.platform(), user_agent_info=request.user_agent.string, **context)


def secured_render(template: str, **context):
    if session.get("user_data") is None:
        return redirect(url_for("login"))
    return render_template_with_base_template(template, **context)


@app.route('/login', methods=['GET'])
def login():
    return render_template_with_base_template("login.html")


@app.route('/login', methods=['POST'])
def login_post():
    user = User(request.form.get("login"), request.form.get("password"))

    with open("users.json", "r") as users_data:
        users = json.load(users_data)

        if user.login in users and user.password == users[user.login]["password"]:
            session["user_data"] = users[user.login]["data"]
            session["user_data"]["login"] = user.login
            return redirect(url_for("info"))

    session["login_message"] = "Check the privilege of entering your login and password"
    return render_template_with_base_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/change_password", methods=["POST"])
def change_password():

    user_login = session["user_data"].get("login")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")

    with open("users.json", "r+") as file:
        users = json.load(file)

        if old_password == users[user_login]["password"]:
            users[user_login]["password"] = new_password
        else:
            session["cookie_message"] = "Enter the correct old password"
            return redirect(url_for("info"))

    with open("users.json", "w") as file:
        json.dump(users, file)

        session["cookie_message"] = "You have successfully changed your password"
        return redirect(url_for("info"))


@app.route("/info")
def info():
    return secured_render("info.html", cookies=request.cookies.items())


@app.route("/add_cookie", methods=["POST"])
def add_cookie():
    cookie_key = request.form.get("cookie_key")
    cookie_value = request.form.get("cookie_value")
    cookie_exp = request.form.get("expires_at")

    response = make_response(redirect(url_for("info")))
    response.set_cookie(cookie_key, cookie_value, expires=cookie_exp)

    session["cookie_message"] = "You added a fancy cookie"

    return response


@app.route("/remove_cookie", methods=["POST"])
def remove_cookie():
    cookie_key = request.form.get("cookie_key")

    response = make_response(redirect(url_for("info")))

    if cookie_key is None:
        for key in request.cookies.keys():
            if key != "session":
                response.delete_cookie(key)

        session["cookie_message"] = "You have given all the cookies"
        return response

    if cookie_key not in request.cookies.keys():
        session["cookie_message"] = f"Undefined {cookie_key}"
        return redirect(url_for('info'))

    response.delete_cookie(cookie_key)
    session["cookie_message"] = f"Unfortunately, we have successfully deleted your cookie {cookie_key}"
    return response


@app.route('/')
@app.route('/portfolio')
def portfolio_main():
    return render_template_with_base_template("portfolio-main.html")


@app.route('/projects')
def portfolio_projects():
    return render_template_with_base_template("portfolio-projects.html", projects_list=PROJECTS_LIST)


@app.route('/contacts')
def portfolio_contacts():
    return render_template_with_base_template("portfolio-contacts.html", contacts=CONTACTS)


@app.route('/skills')
@app.route('/skills/<int:id>')
def portfolio_skills(id: int = None):
    if id is not None:
        return render_template_with_base_template("portfolio-skills.html", selected_skill=SKILLS_LIST[id])

    return render_template_with_base_template("portfolio-skills.html", all_skills_list=SKILLS_LIST)
