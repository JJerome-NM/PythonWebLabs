# from flask_wtf import FlaskForm
# from wtforms import StringField, SubmitField
# from wtforms.validators import DataRequired
#
# from app import db
#
#
# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(30), unique=False, nullable=False)
#     comment = db.Column(db.String(2048), nullable=False)
#     date = db.Column(db.String(50))
#
#
# class CommentForm(FlaskForm):
#     comment = StringField("", validators=[DataRequired(message="This field is required.")])
#     submit = SubmitField("Comment")
