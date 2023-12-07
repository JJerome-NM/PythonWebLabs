from datetime import date

import pytest
from flask import url_for

from app import create_app, db
from app.authentication.entitys import AuthUser
from app.posts.entitys import Tag, Category, Post, PostType
from config import TestConfig


@pytest.fixture(scope='module')
def client():
    app = create_app(TestConfig)

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture(scope='module')
def tags():
    tags = [Tag(name='games'),  Tag(name='coding'),  Tag(name='video'),  Tag(name='tests')]
    yield tags


@pytest.fixture(scope='module')
def categories():
    categories = [Category(name='Development'), Category(name='Java'), Category(name="Test")]
    yield categories


@pytest.fixture(scope='module')
def posts(categories, tags):
    yield [
        Post(title='New post test 1', text='New post test 1', created=date(2023, 12, 7),
             type=PostType.OTHER, enable=True, category=categories[0], tags=[tags[0]], user_id=0),

        Post(title='New post test 2', text='New post test 2', created=date(2023, 12, 7),
             type=PostType.NEWS, enable=True, category=categories[0], tags=[tags[0], tags[1]], user_id=0),

        Post(title='New post test 3', text='New post test 3', created=date(2023, 12, 7),
             type=PostType.PUBLICATION, enable=False, category=categories[1], tags=[tags[2], tags[3]], user_id=0)
    ]


@pytest.fixture(scope='module')
def default_user():
    user = AuthUser(email='test_user@gmail.com', username='test_user', password='testpass')
    yield user

@pytest.fixture(scope='module')
def init_db(default_user, posts, categories):
    db.create_all()

    user: AuthUser = AuthUser(
        email="test_user2@gmail.com",
        username="test_user2",
        password="testpass"
    )

    user.posts = [posts[2]]
    default_user.posts = [posts[0], posts[1]]

    db.session.add_all([default_user, user])

    for category in categories:
        db.session.add(category)

    db.session.commit()

    yield


@pytest.fixture(scope='function')
def auth_user(client, default_user):
    client.post(
        url_for('auth.login'),
        data={'email': default_user.email, 'password': 'testpass'},
        follow_redirects=True
    )

    yield default_user

    client.post(url_for('auth.logout'))
