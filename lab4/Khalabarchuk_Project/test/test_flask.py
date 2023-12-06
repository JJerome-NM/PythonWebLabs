import unittest

from flask_testing import TestCase

import config
from app import create_app, db

from app.authentication.entitys import AuthUser


class TestBase(TestCase):
    def create_app(self):
        app = create_app(config.TestConfig)
        return app

    def setUp(self):
        db.create_all()
        user = AuthUser(
            email="test_user@gmail.com",
            username="test_user",
            password="testpass"
        )
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_setup(self):
        self.assertTrue(self.app is not None)
        self.assertTrue(self.client is not None)
        self.assertTrue(self._ctx is not None)


if __name__ == '__main__':
    unittest.main()
