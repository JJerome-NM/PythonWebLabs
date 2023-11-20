from flask import redirect, url_for, flash
from flask_login import login_required

from app import db
from ..common_logic import base_render
from .forms import ToDoForm
from .entitys import ToDo

from . import todo_bp


@todo_bp.route('/todo', methods=["GET"])
@login_required
def todo_page():
    return base_render("todo-page.html", todo_list=ToDo.query.all(), todo_form=ToDoForm())


@todo_bp.route("/todo", methods=["POST"])
@login_required
def add_todo():
    todo_form = ToDoForm()
    if todo_form.validate_on_submit():
        new_todo = ToDo(title=todo_form.title.data, completed=False, status=ToDo.Status.IN_PROGRESS)
        db.session.add(new_todo)
        db.session.commit()

        flash('Todo added successfully', 'success')

    return redirect(url_for("todo.todo_page"))


@todo_bp.route("/todo/<string:id>")
@login_required
def delete_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')

    return redirect(url_for("todo.todo_page"))


@todo_bp.route("/todo/<string:id>/update")
@login_required
def update_todo(id: str):
    todo = db.get_or_404(ToDo, id)
    todo.complete()

    db.session.commit()
    flash('Todo updated successfully', 'success')

    return redirect(url_for("todo.todo_page"))
