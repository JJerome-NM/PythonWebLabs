from flask import Blueprint
from flask_wtf import CSRFProtect

api_todo_bp = Blueprint("api_todo", __name__)

from . import controller
