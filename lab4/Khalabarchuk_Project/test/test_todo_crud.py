import unittest

from flask import url_for
from flask_login import current_user

from app import db
from app.todo.entitys import ToDo
from test.test_flask import TestBase


class TestTodoCRUD(TestBase):

    def test_user_login(self):
        """Test the user login process."""
        # Check if a user can successfully log in and if the login status is reflected correctly.

        with self.client:
            response = self.client.post(
                url_for("auth.login"),
                data=dict(
                    login="test_user@gmail.com",
                    password="testpass",
                    remember=True
                ),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertNotIn(
                f'<form action="{url_for("auth.login")}" method="post" class="login-form" novalidate>',
                response.text)

            self.assertTrue(current_user.is_authenticated)

    def test_todo_page(self):
        self.test_user_login()

        with self.client:
            todo_1 = ToDo(title="New todo 1", completed=False, status="IN_PROGRESS")

            db.session.add(todo_1)
            db.session.commit()

            response = self.client.get(
                url_for("todo.todo_page"),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertIn(f'action="{url_for("todo.add_todo")}"', response.text)
            self.assertIn(f'<a href="{url_for("todo.update_todo", id=ToDo.query.first().id)}"', response.text)

    def test_todo_create(self):
        self.test_user_login()

        with self.client:
            response = self.client.post(
                url_for("todo.add_todo"),
                data=dict(
                    title="New test todo4422666"
                ),
                follow_redirects=True
            )

            todo: ToDo = ToDo.query.filter_by(title="New test todo4422666").first()

            self.assert200(response)
            self.assertEqual(todo.status, ToDo.Status.IN_PROGRESS)
            self.assertFalse(todo.completed)

    def test_todo_delete(self):
        self.test_user_login()

        with self.client:
            todo_1 = ToDo(title="New todo 1", completed=False, status="IN_PROGRESS")

            db.session.add(todo_1)
            db.session.commit()

            response = self.client.get(
                url_for("todo.delete_todo", id=todo_1.id),
                follow_redirects=True
            )

            todo = ToDo.query.get(todo_1.id)

            self.assert200(response)
            self.assertIsNone(todo)

    def test_todo_update(self):
        self.test_user_login()

        with self.client:
            todo_1 = ToDo(title="New todo 1", completed=False, status="IN_PROGRESS")

            db.session.add(todo_1)
            db.session.commit()

            response = self.client.get(
                url_for("todo.update_todo", id=todo_1.id),
                follow_redirects=True
            )

            todo: ToDo = ToDo.query.get(todo_1.id)

            self.assert200(response)
            self.assertIsNotNone(todo)
            self.assertTrue(todo.completed)


if __name__ == '__main__':
    unittest.main()
