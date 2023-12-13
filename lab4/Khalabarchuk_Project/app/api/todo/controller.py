from ... import db
from ...todo.entitys import ToDo

from . import api_todo_bp
from ...todo.forms import ToDoForm

from ..auth.JWTUtils import JWTUtils

@api_todo_bp.get("/")
@JWTUtils.verify_token
def get_all_todos():
    return [t.to_dict() for t in ToDo.query.all()], 200


@api_todo_bp.post("/")
@JWTUtils.verify_token
def create_todo():
    todo_form = ToDoForm(meta={'csrf': False})
    if todo_form.validate_on_submit():
        new_todo = ToDo(title=todo_form.title.data, completed=False, status=ToDo.Status.IN_PROGRESS)
        db.session.add(new_todo)
        db.session.commit()

        return new_todo.to_dict(), 201

    return todo_form.form_errors, 400


@api_todo_bp.get("/<int:id>")
@JWTUtils.verify_token
def get_todo(id):
    return ToDo.query.get_or_404(id).to_dict(), 200


@api_todo_bp.put("/<int:id>")
@JWTUtils.verify_token
def update_todo(id):
    todo = ToDo.query.get_or_404(id)
    todo.complete()

    db.session.commit()

    return todo.to_dict(), 200


@api_todo_bp.delete("/<int:id>")
@JWTUtils.verify_token
def delete_todo(id):
    todo = ToDo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()

    return dict(
        message="Todo deleted"
    ), 200

