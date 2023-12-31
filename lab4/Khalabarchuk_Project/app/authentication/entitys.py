import datetime
import os.path
import secrets

from flask_login import UserMixin

from PIL import Image

from app import db, bcrypt, login_manager, config


class AuthUser(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), unique=False, nullable=False)
    avatar_image = db.Column(db.String(30), nullable=True, default=config.AVATAR_DEFAULT)
    about_me = db.Column(db.String(500), nullable=True, default="")
    last_seen = db.Column(db.DateTime, nullable=True, default=datetime.datetime.now().replace(microsecond=0))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password=password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def set_avatar_image(self, new_image):
        new_avatar_name = AuthUser.save_new_user_avatar(new_image)
        if self.avatar_image != config.AVATAR_DEFAULT:
            AuthUser.delete_old_user_avatar(self.avatar_image)

        self.avatar_image = new_avatar_name

    @staticmethod
    @login_manager.user_loader
    def user_loader(user_id: int):
        return AuthUser.query.get(user_id)

    @staticmethod
    def delete_old_user_avatar(picture_name: str):
        avatar_path = os.path.join(config.AVATARS_DIR_PATH, picture_name)

        if os.path.exists(avatar_path):
            os.remove(avatar_path)

    @staticmethod
    def save_new_user_avatar(picture) -> str:
        avatar_hex = secrets.token_hex(20)

        f_name, f_ext = os.path.splitext(picture.filename)
        avatar_file_name = f"{avatar_hex}{f_ext}"
        avatar_path = os.path.join(config.AVATARS_DIR_PATH, avatar_file_name)

        out_size = (1024, 1024)
        image = Image.open(picture)
        image.thumbnail(out_size)
        image.save(avatar_path)

        return avatar_file_name
