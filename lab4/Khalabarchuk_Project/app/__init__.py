from flask import Flask
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_marshmallow import Marshmallow

from config import Config

from .common_logic import enumerate_filter

db = SQLAlchemy()
mm = Marshmallow()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=Config.get_config()):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)

    db.init_app(app)
    mm.init_app(app)
    bcrypt.init_app(app)

    app.jinja_env.filters['enumerate'] = enumerate_filter

    login_manager.init_app(app)
    login_manager.login_view = config_class.LOGIN_MANAGER_LOGIN_VIEW
    login_manager.login_message_category = config_class.LOGIN_MANAGER_LOGIN_MESSAGE_CATEGORY
    login_manager.login_message = config_class.LOGIN_MANAGER_LOGIN_MESSAGE

    with app.app_context():
        from .authentication import auth_bp
        from .user import user_bp
        from .common import common_bp
        from .cookie import cookie_bp
        from .todo import todo_bp
        from .posts import posts_bp
        from .api import api_bp

        app.register_blueprint(api_bp, url_prefix="/api")
        app.register_blueprint(auth_bp, url_prefix="/auth")
        app.register_blueprint(user_bp, url_prefix="/user")
        app.register_blueprint(common_bp, url_prefix="/common")
        app.register_blueprint(cookie_bp, url_prefix="/cookie")
        app.register_blueprint(todo_bp, url_prefix="/todo")
        app.register_blueprint(posts_bp, url_prefix="/post")

        from . import views

    return app


config = Config.get_config()

app = create_app(config)

Migrate(app, db)
