from flask import redirect, url_for, flash
from flask_login import login_required, current_user

from .forms import *
from .entitys import *

from ..common_logic import base_render

from . import posts_bp


@posts_bp.route("/")
@login_required
def all_posts():
    return base_render("all-post.html", posts=Post.query.all())


@posts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreateEditPostForm()

    if form.validate_on_submit():
        post = form.build_post()
        db.session.add(post)
        db.session.commit()

    return base_render("edit-post.html", form=form, form_title="Create post❤️‍🩹")


@posts_bp.route("/{int:id}")
@login_required
def get_post(id):
    return base_render("all-post.html", posts=Post.query.get(id))


@posts_bp.route("/{int:id}/update", methods=["GET", "POST"])
@login_required
def update_post(id):
    form = CreateEditPostForm()

    if form.validate_on_submit():
        post = form.build_post()
        db.session.add(post)
        db.session.commit()

    return base_render("edit-post.html", form=form, form_title="Edit post‍🐍")


@posts_bp.route("/{int:id}/delete")
@login_required
def delete_post(id):
    post: Post = Post.query.get(id)

    if post.user_id != current_user.id:
        flash("Ви повинні бути власником поста щоб його видалити", "danger")
        redirect(url_for("post.get_post", id=id))

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("post.all_posts"))
