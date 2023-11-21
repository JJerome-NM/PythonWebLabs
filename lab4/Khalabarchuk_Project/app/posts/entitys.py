import os
import secrets
from datetime import datetime
from enum import Enum

from PIL import Image

from .. import db, config


class PostType(Enum):
    NEWS = "NEWS"
    PUBLICATION = "PUBLICATION"
    OTHER = "OTHER"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(90))
    text = db.Column(db.String(2056))
    image = db.Column(db.String(35), nullable=False, default=config.POST_IMAGE_DEFAULT)
    created = db.Column(db.DateTime, nullable=True, default=datetime.now().replace(microsecond=0))
    type = db.Column(db.Enum(PostType), nullable=False, default=PostType.OTHER)
    enable = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.ForeignKey("auth_user.id"), nullable=False)

    def set_avatar_image(self, new_image):
        new_image_name = Post.save_new_post_image(new_image)
        if self.image != config.POST_IMAGE_DEFAULT:
            Post.delete_old_post_image(self.image)

        self.image = new_image_name

    @staticmethod
    def delete_old_post_image(image_name: str):
        if not image_name:
            return

        image_path = os.path.join(config.POST_IMAGES_DIR_PATH, image_name)

        if os.path.exists(image_path):
            os.remove(image_path)

    @staticmethod
    def save_new_post_image(picture) -> str:
        picture_hex = secrets.token_hex(25)

        f_name, f_ext = os.path.splitext(picture.filename)
        picture_file_name = f"{picture_hex}{f_ext}"
        picture_path = os.path.join(config.POST_IMAGES_DIR_PATH, picture_file_name)

        out_size = (1024, 1024)
        image = Image.open(picture)
        image.thumbnail(out_size)
        image.save(picture_path)

        return picture_file_name
