from flask import redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import desc

from .forms import *
from .entitys import *

from ..common_logic import base_render

from . import posts_bp


@posts_bp.route("/", methods=["GET", "POST"])
@login_required
def all_posts():
    form = SearchPostForm()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", config.POSTS_MAX_PER_PAGE, type=int)
    category = request.args.get("category", "ANY") if request.method == "GET" else form.category.data
    posts = Post.query

    if (form.validate_on_submit() or request.method == "GET") and category != "ANY":
        form.category.data = category
        posts = posts.filter(Post.category.has(id=form.category.data))

    posts = posts.order_by(desc(Post.created)).paginate(page=page, per_page=per_page)

    return base_render("all-posts.html", posts=posts, form=form)


@posts_bp.route("/<int:id>")
@login_required
def get_post(id):
    post = Post.query.get(id)

    if not post:
        flash("Post not found", "warning")
        return redirect(url_for("posts.all_posts"))

    return base_render("post.html", post=post)


@posts_bp.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = CreateEditPostForm()

    if form.validate_on_submit():
        post = form.build_post()
        db.session.add(post)
        db.session.commit()

        return redirect(url_for("posts.get_post", id=post.id))

    flash("Post successfully established", "success")
    return base_render("edit-post.html",
                       form=form,
                       form_title="Create post❤️‍🩹",
                       form_action=url_for("posts.create_post"))


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

        flash("You have successfully update a post", "success")
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
        flash("You must be the owner of the post to delete it", "danger")
        return redirect(url_for("posts.get_post", id=id))

    db.session.delete(post)
    db.session.commit()

    flash("Post successfully deleted", "success")
    return redirect(url_for("posts.all_posts"))


@posts_bp.route("/categories")
@login_required
def categories():
    categories_with_forms = [{"id": c.id, "form": CreateEditCategory(name=c.name)} for c in Category.query.all()]
    form = CreateEditCategory()
    return base_render("all-categories.html", categories=categories_with_forms, form=form)


@posts_bp.route("/category/<int:id>/update", methods=["POST"])
def category_update(id):
    form = CreateEditCategory()

    if form.validate_on_submit():
        category = db.get_or_404(Category, id)

        category.name = form.name.data
        db.session.commit()
        flash("You have successfully update a category", "success")

    return redirect(url_for("posts.categories"))


@posts_bp.route("/category/<int:id>/delete", methods=["GET"])
def category_delete(id):
    db.session.delete(db.get_or_404(Category, id))
    db.session.commit()

    flash("Category successfully deleted", "success")
    return redirect(url_for("posts.categories"))


@posts_bp.route("/category/create", methods=["POST"])
def category_create():
    form = CreateEditCategory()

    if form.validate_on_submit():
        category = Category(name=form.name.data)

        db.session.add(category)
        db.session.commit()

    flash("Category successfully established", "success")
    return redirect(url_for("posts.categories"))
