from flask import Blueprint

api_todo_bp = Blueprint("api_todo", __name__)

from . import controller
