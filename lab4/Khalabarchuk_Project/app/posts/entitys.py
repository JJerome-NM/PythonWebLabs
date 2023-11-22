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


tags = db.Table('post_tag',
                db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                )


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(90))
    text = db.Column(db.String(2056))
    image = db.Column(db.String(35), nullable=False, default=config.POST_IMAGE_DEFAULT)
    created = db.Column(db.DateTime, nullable=True, default=datetime.now().replace(microsecond=0))
    type = db.Column(db.Enum(PostType), nullable=False, default=PostType.OTHER)
    enable = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.ForeignKey("auth_user.id"), nullable=False)
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))
    category_id = db.Column(db.ForeignKey('category.id'))
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def update(self, form):
        self.title = form.title.data
        self.text = form.text.data
        self.type = form.type.data
        self.enable = form.enable.data
        self.tags = [t for t in Tag.query.filter(Tag.name.in_(form.tags.data)).all()]
        self.category_id = form.category.data

        self.set_post_image(form.image.data)

    def set_post_image(self, new_image):
        if not new_image and self.image:
            return

        if not self.image and not new_image:
            self.image = config.POST_IMAGE_DEFAULT
            return

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


class CategoryCRUD:

    @staticmethod
    def create_category(name):
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def read_categories():
        return Category.query.all()

    @staticmethod
    def read_category(category_id):
        return Category.query.get(category_id)

    @staticmethod
    def update_category(category_id, name):
        category = Category.query.get(category_id)
        if category:
            category.name = name
            db.session.commit()
            return category
        return None

    @staticmethod
    def delete_category(category_id):
        category = Category.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False
