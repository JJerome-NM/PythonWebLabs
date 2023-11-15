from flask import Blueprint

cookie_bp = Blueprint("cookie", __name__, template_folder="templates/cookie")

from . import views
