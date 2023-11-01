from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

from app import db


class ToDoForm(FlaskForm):
    title = StringField("", validators=[DataRequired(message="This field is required.")])
    submit = SubmitField("Save")


class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    completed = db.Column(db.Boolean)
    status = db.Column(db.String(20))

    def complete(self):
        self.completed = True
        self.status = ToDo.Status.COMPLETED

    class Status:
        COMPLETED = "COMPLETED"
        IN_PROGRESS = "IN_PROGRESS"

