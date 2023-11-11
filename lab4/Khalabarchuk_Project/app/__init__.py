from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

import config

def enumerate_filter(iterable):
    return enumerate(iterable)


app = Flask(__name__)
app.secret_key = b"secret"

app.config.from_object('config')

app.jinja_env.filters['enumerate'] = enumerate_filter

db = SQLAlchemy(app)

migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = config.LOGIN_MANAGER_LOGIN_VIEW
login_manager.login_message_category = config.LOGIN_MANAGER_LOGIN_MESSAGE_CATEGORY
login_manager.login_message = config.LOGIN_MANAGER_LOGIN_MESSAGE

from app import views
from app.controller import CommentController
from app.controller import CookieController
from app.controller import UserController