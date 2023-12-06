import unittest

from flask import url_for

from app import db
from app.authentication.entitys import AuthUser
from test.test_flask import TestBase


class TestUser(TestBase):

    def test_user_registered(self):
        user: AuthUser = AuthUser.query.filter_by(email='test_user@gmail.com').first()
        self.assertEqual(user.username, "test_user")
        self.assertEqual(user.email, "test_user@gmail.com")
        self.assertTrue(user.verify_password("testpass"))

    def test_user_create(self):
        with self.client:
            response = self.client.post(
                url_for("auth.sign_up"),
                data=dict(
                    username="test_user2",
                    email="test_user2@gmail.com",
                    password="test_pass",
                    confirm_password="test_pass"
                ),
                follow_redirects=True
            )
            self.assert200(response)

            user = AuthUser.query.filter_by(email="test_user2@gmail.com").first()

            self.assertIsNotNone(user)
            self.assertEqual(user.email, "test_user2@gmail.com")
            self.assertEqual(user.username, "test_user2")
            self.assertNotEqual(user.password_hash, "password")

    def test_user_id(self):
        user: AuthUser = AuthUser.query.filter_by(email="test_user@gmail.com").first()

        self.assertTrue(user.id == 1)
        self.assertFalse(user.id == 1337)


if __name__ == '__main__':
    unittest.main()
