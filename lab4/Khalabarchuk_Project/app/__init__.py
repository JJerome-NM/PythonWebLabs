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


def create_app(config_class):
    app_with_bp = Flask(__name__, instance_relative_config=True)

    app_with_bp.config.from_object(config_class)

    app_with_bp.secret_key = b"secret"

    app_with_bp.jinja_env.filters['enumerate'] = enumerate_filter

    with app_with_bp.app_context():
        db.init_app(app_with_bp)
        bcrypt.init_app(app_with_bp)
        login_manager.init_app(app_with_bp)

        from .user import user_bp
        app_with_bp.register_blueprint(user_bp, url_prefix="/user")

        from .authentication import auth_bp
        app_with_bp.register_blueprint(auth_bp, url_prefix="/auth")

        from .common import common_bp
        app_with_bp.register_blueprint(common_bp, url_prefix="/common")

        from .cookie import cookie_bp
        app_with_bp.register_blueprint(cookie_bp, url_prefix="/cookie")

        from .todo import todo_bp
        app_with_bp.register_blueprint(todo_bp, url_prefix="/todo")

    return app_with_bp


app = create_app("config")
