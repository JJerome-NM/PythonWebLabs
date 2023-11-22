from flask import redirect, url_for, flash, request
from flask_login import login_required

from .forms import *
from .entitys import *

from ..common_logic import base_render

from . import posts_bp


@posts_bp.route("/", methods=["GET", "POST"])
@login_required
def all_posts():
    form = SearchPostForm()

    if request.method == 'POST' and form.validate():
        if form.category.data == "ANY":
            posts = Post.query.all()
        else:
            posts = Post.query.filter(Post.category.has(id=form.category.data)).all()
    else:
        posts = Post.query.all()

    return base_render("all-posts.html", posts=posts, form=form)


@posts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreateEditPostForm()

    if form.validate_on_submit():
        post = form.build_post()
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("posts.get_post", id=post.id))

    return base_render("edit-post.html",
                       form=form,
                       form_title="Create post❤️‍🩹",
                       form_action=url_for("posts.create_post"))


@posts_bp.route("/<int:id>")
@login_required
def get_post(id):
    post = Post.query.get(id)

    if not post:
        flash("Post not found", "warning")
        return redirect(url_for("posts.all_posts"))

    return base_render("post.html", post=post)



@posts_bp.route("/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_post(id):
    post: Post = Post.query.get(id)

    if not post:
        flash("Post not found", "warning")
        return redirect(url_for("posts.all_posts"))

    form = CreateEditPostForm()

    if form.validate_on_submit():
        post.update(form)

        db.session.commit()

        return redirect(url_for("posts.get_post", id=post.id))
    else:
        form.build_edit_form(post)

    return base_render("edit-post.html",
                       form=form,
                       form_title="Edit post‍🐍",
                       form_action=url_for("posts.update_post", id=post.id))


@posts_bp.route("/<int:id>/delete", methods=["GET"])
@login_required
def delete_post(id):
    post: Post = db.get_or_404(Post, id)

    if post.user_id != current_user.id:
        flash("Ви повинні бути власником поста щоб його видалити", "danger")
        return redirect(url_for("posts.get_post", id=id))

    db.session.delete(post)
    db.session.commit()

    return redirect(url_for("posts.all_posts"))
