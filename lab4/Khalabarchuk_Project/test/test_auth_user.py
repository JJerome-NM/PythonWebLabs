import unittest

from flask import url_for
from flask_login import current_user

from app import db
from app.authentication.entitys import AuthUser
from test.test_flask import TestBase


class TestUser(TestBase):

    def test_user_registered(self):
        """Test the registration of a user and verify the user's attributes."""
        # Check if a user with specified details is correctly registered and has the expected attributes.

        user: AuthUser = AuthUser.query.filter_by(email='test_user@gmail.com').first()
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test_user@gmail.com")
        self.assertTrue(user.verify_password("testpass"))

    def test_user_registration_page(self):
        """Test the rendering of the user registration page."""
        # Check if the user registration page is rendered correctly.

        with self.client:
            response = self.client.get(
                url_for("auth.sign_up"),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertIn(
                f'<form action="{url_for("auth.sign_up")}" method="post"',
                response.text)

    def test_user_registration(self):
        """Test the user registration process."""
        # Check if a user can successfully register and verify the attributes of the registered user.

        with self.client:
            response = self.client.post(
                url_for("auth.sign_up"),
                data=dict(
                    username="test_user2",
                    email="test_user2@gmail.com",
                    password="testpass",
                    confirm_password="testpass"
                ),
                follow_redirects=True
            )
            self.assert200(response)

            user = AuthUser.query.filter_by(email="test_user2@gmail.com").first()

            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test_user2@gmail.com")
            self.assertEqual(user.username, "test_user2")
            self.assertTrue(user.verify_password("testpass"))

    def test_user_login_page(self):
        """Test the rendering of the user login page."""
        # Check if the user login page is rendered correctly.

        with self.client:
            response = self.client.get(
                url_for("auth.login"),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertIn(
                f'<form action="{url_for("auth.login")}" method="post" class="login-form" novalidate>',
                response.text)

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

    def test_user_details_change_page(self):
        """Test the rendering and functionality of the user details change page."""
        # Check if the user details change page is rendered correctly and if user details can be successfully updated.

        self.test_user_login()

        with self.client:
            response = self.client.post(
                url_for("user.account"),
                data=dict(
                    username="test_user_new",
                    email="test_user_new@gmail.com",
                    about_me="New about me",
                    old_password="testpass",
                ),
                follow_redirects=True
            )

            self.assert200(response)
            self.assertNotIn(f'<form action="{url_for("user.account")}" method="post"', response.text)
            self.assertTrue(current_user.is_authenticated)

            user: AuthUser = AuthUser.query.filter_by(email="test_user_new@gmail.com").first()

            self.assertEqual(user.username, "test_user_new")
            self.assertEqual(user.email, "test_user_new@gmail.com")
            self.assertEqual(user.about_me, "New about me")


if __name__ == '__main__':
    unittest.main()
