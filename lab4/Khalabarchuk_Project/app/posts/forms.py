from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

from .entitys import PostType, Post


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
    enable = BooleanField("Published")
    submit = SubmitField("Save")

    def build_post(self) -> Post:
        post = Post(
            title=self.title.data,
            text=self.text.data,
            type=self.type.data,
            enable=self.enable.data,
            user_id=current_user.id
        )

        post.set_avatar_image(self.image.data)

        return post
