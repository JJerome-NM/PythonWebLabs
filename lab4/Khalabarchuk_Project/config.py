from os import environ


class Config(object):
    FLASK_DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = environ.get('SECRET_KEY') or 'secret'
    FLASK_SECRET = SECRET_KEY

    # Login manager
    LOGIN_MANAGER_LOGIN_VIEW = "auth.login"
    LOGIN_MANAGER_LOGIN_MESSAGE_CATEGORY = "info"
    LOGIN_MANAGER_LOGIN_MESSAGE = "You need to be logged-in to access this page"

    # User avatars
    AVATARS_DIR_PATH = "./app/static/users-avatars"
    AVATAR_DEFAULT = "default.png"

    # Posts images
    POST_IMAGES_DIR_PATH = "./app/static/post-images"
    POST_IMAGE_DEFAULT = "post_default.gif"

    # SQLALCHEMY
    SQLALCHEMY_DATABASE_URI = (environ.get('SQLALCHEMY_DATABASE_URI') or
                               'postgresql://postgres:postgres@localhost:5432/postgres')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLALCHEMY Pagination
    POSTS_MAX_PER_PAGE = 1

    @staticmethod
    def get_config():
        return config[environ.get('CONFIG') or "DEFAULT"]


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProdConfig(Config):
    DEVELOPMENT = False
    DEBUG = False


class TestConfig(Config):
    # Server
    SERVER_NAME = "localhost:5000"
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///testdb.db")


config = {
    'TEST': TestConfig,
    'DEV': DevConfig,
    'PROD': ProdConfig,
    'DEFAULT': DevConfig,
}
