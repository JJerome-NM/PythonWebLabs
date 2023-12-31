from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from flask_wtf.form import _Auto
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms.widgets import CheckboxInput, ListWidget

from .entitys import PostType, Post, Category, Tag


class CreateEditCategory(FlaskForm):
    name = StringField("name", validators=[
        DataRequired("This field is required"),
        Length(4, 40, "The length must be greater than 4 and less than 90")
    ])
    submit = SubmitField("Save")

    def validate_name(self, field):
        if Category.query.filter(Category.name.ilike(field.data)).first():
            raise ValidationError("The category with this name is already busy")


class SearchPostForm(FlaskForm):
    category = SelectField("Category", default="ANY")
    submit = SubmitField("Search")

    def __init__(self, *args, **kwargs):
        super(SearchPostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()] + [("ANY", "Any")]


class CreateEditPostForm(FlaskForm):
    title = StringField("Title", validators=[
        DataRequired("This field is required"),
        Length(4, 90, "The length must be greater than 4 and less than 90")
    ])
    text = TextAreaField("Post text", validators=[
        DataRequired("This field is required"),
        Length(0, 2000, "The length must be greater than 0 and less than 2000")
    ])
    image = FileField("Post picture", validators=[
        FileAllowed(["jpg", "png", "jfif", "gif"])
    ])
    type = SelectField("Type", choices=[(c.name, c.value) for c in PostType])
    category = SelectField("Category", choices=[(c.id, c.name) for c in Category.query.all()])
    tags = SelectMultipleField("Tags", choices=[(t.name, t.name) for t in Tag.query.all()],
                               option_widget=CheckboxInput(), widget=ListWidget(prefix_label=False))
    enable = BooleanField("Published")
    submit = SubmitField("Save")

    def __init__(self, *args, **kwargs):
        super(CreateEditPostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(c.id, c.name) for c in Category.query.all()]
        self.tags.choices = [(t.name, t.name) for t in Tag.query.all()]

    def build_post(self) -> Post:
        post = Post(
            title=self.title.data,
            text=self.text.data,
            type=self.type.data,
            enable=self.enable.data,
            category_id=self.category.data,
            tags=[t for t in Tag.query.filter(Tag.name.in_(self.tags.data)).all()],
            user_id=current_user.id
        )

        post.set_post_image(self.image.data)

        return post

    def build_edit_form(self, post: Post):
        self.title.data = post.title
        self.type.default = post.type.name
        self.text.data = post.text
        self.enable.data = post.enable
        self.category.data = post.category
        self.tags.data = [t.name for t in post.tags]
