from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

from .common_logic import enumerate_filter


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class=Config.get_config()):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)

    db.init_app(app)

    Migrate(app, db)

    bcrypt.init_app(app)

    app.jinja_env.filters['enumerate'] = enumerate_filter

    login_manager.init_app(app)
    login_manager.login_view = config_class.LOGIN_MANAGER_LOGIN_VIEW
    login_manager.login_message_category = config_class.LOGIN_MANAGER_LOGIN_MESSAGE_CATEGORY
    login_manager.login_message = config_class.LOGIN_MANAGER_LOGIN_MESSAGE

    with app.app_context():

        from .user import user_bp
        app.register_blueprint(user_bp, url_prefix="/user")

        from .authentication import auth_bp
        app.register_blueprint(auth_bp, url_prefix="/auth")

        from .common import common_bp
        app.register_blueprint(common_bp, url_prefix="/common")

        from .cookie import cookie_bp
        app.register_blueprint(cookie_bp, url_prefix="/cookie")

        from .todo import todo_bp
        app.register_blueprint(todo_bp, url_prefix="/todo")

    return app
