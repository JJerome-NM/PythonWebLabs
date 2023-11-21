from datetime import datetime

from flask import request, flash, redirect, url_for
from flask_login import login_required, current_user

# from ..authentication.forms import ChangePasswordForm
from app import db

from ..common_logic import base_render

from . import common_bp
from .entitys import Comment
from .forms import CommentForm

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


@common_bp.route("/comments")
@login_required
def comments_page():
    return base_render("comments-page.html", comment_form=CommentForm(), comments=Comment.query.all())


@common_bp.route("/comments", methods=["POST"])
@login_required
def add_comment():
    comment_form = CommentForm()

    if comment_form.validate_on_submit():
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_comment = Comment(username=current_user.username, comment=comment_form.comment.data, date=date)
        db.session.add(new_comment)
        db.session.commit()

        flash('Comment added successfully', 'success')
    else:
        flash('Something went wrong while adding a comment', 'danger')

    return redirect(url_for("common.comments_page"))


@common_bp.route("/info")
@login_required
def info():
    return base_render("info.html", cookies=request.cookies.items())


@common_bp.route('/')
@common_bp.route('/portfolio')
def portfolio_main():
    return base_render("portfolio-main.html")


@common_bp.route('/projects')
def portfolio_projects():
    return base_render("portfolio-projects.html", projects_list=PROJECTS_LIST)


@common_bp.route('/contacts')
def portfolio_contacts():
    return base_render("portfolio-contacts.html", contacts=CONTACTS)


@common_bp.route('/skills')
@common_bp.route('/skills/<int:id>')
def portfolio_skills(id: int = None):
    if id is not None:
        return base_render("portfolio-skills.html", selected_skill=SKILLS_LIST[id])

    return base_render("portfolio-skills.html", all_skills_list=SKILLS_LIST)
