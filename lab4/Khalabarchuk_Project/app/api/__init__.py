from flask import Blueprint

api_bp = Blueprint("api", __name__)

from .todo import api_todo_bp
from .auth import api_auth_bp
from .user import api_user_bp
from . import controller

api_bp.register_blueprint(api_todo_bp, url_prefix="/todo")
api_bp.register_blueprint(api_auth_bp, url_prefix="/auth")
api_bp.register_blueprint(api_user_bp, url_prefix="/users")
