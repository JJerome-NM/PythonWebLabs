# from flask import request, make_response, redirect, url_for, flash
# from flask_login import login_required
#
# from app import app
#
#
# @app.route("/add_cookie", methods=["POST"])
# @login_required
# def add_cookie():
#     cookie_key = request.form.get("cookie_key")
#     cookie_value = request.form.get("cookie_value")
#     cookie_exp = request.form.get("expires_at")
#
#     response = make_response(redirect(url_for("info")))
#     response.set_cookie(cookie_key, cookie_value, expires=cookie_exp)
#
#     flash("You added a fancy cookie", "info")
#     return response
#
#
# @app.route("/remove_cookie", methods=["POST"])
# @login_required
# def remove_cookie():
#     cookie_key = request.form.get("cookie_key")
#
#     response = make_response(redirect(url_for("info")))
#
#     if cookie_key is None:
#         for key in request.cookies.keys():
#             if key != "session":
#                 response.delete_cookie(key)
#
#         flash("You have given all the cookies", "info")
#         return response
#
#     if cookie_key not in request.cookies.keys():
#         flash(f"Undefined {cookie_key}", "danger")
#         return redirect(url_for('info'))
#
#     response.delete_cookie(cookie_key)
#     flash(f"Unfortunately, we have successfully deleted your cookie {cookie_key}", "warning")
#     return response
