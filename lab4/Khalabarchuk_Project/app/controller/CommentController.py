# from datetime import datetime
#
# from flask import flash, redirect, url_for
# from flask_login import login_required, current_user
#
# from app import app, db
# from app.views import base_render
# from entitys.Comment import CommentForm, Comment
#
#
# @app.route("/comments")
# @login_required
# def comments_page():
#     return base_render("comments-page.html", comment_form=CommentForm(), comments=Comment.query.all())
#
#
# @app.route("/comments", methods=["POST"])
# @login_required
# def add_comment():
#     comment_form = CommentForm()
#
#     if comment_form.validate_on_submit():
#         date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#
#         new_comment = Comment(username=current_user.username, comment=comment_form.comment.data, date=date)
#         db.session.add(new_comment)
#         db.session.commit()
#
#         flash('Comment added successfully', 'success')
#     else:
#         flash('Something went wrong while adding a comment', 'danger')
#
#     return redirect(url_for("comments_page"))
