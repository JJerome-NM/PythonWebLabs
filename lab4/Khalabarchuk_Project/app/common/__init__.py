from flask import Blueprint


common_bp = Blueprint("common", __name__, template_folder="templates/common")

from . import views
