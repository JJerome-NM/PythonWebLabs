from os import environ


class Config(object):
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = environ.get('SECRET_KEY') or \
                 '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    FLASK_SECRET = SECRET_KEY

    # Login manager
    LOGIN_MANAGER_LOGIN_VIEW = "auth.login"
    LOGIN_MANAGER_LOGIN_MESSAGE_CATEGORY = "info"
    LOGIN_MANAGER_LOGIN_MESSAGE = "You need to be logged-in to access this page"

    # User avatars
    AVATARS_DIR_PATH = "./app/static/users-avatars"
    AVATAR_DEFAULT = "default.png"

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def get_config():
        return config[environ.get('CONFIG') or "DEFAULT"]


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


config = {
    'DEV': DevConfig,
    'PROD': ProdConfig,
    'DEFAULT': DevConfig,
}
