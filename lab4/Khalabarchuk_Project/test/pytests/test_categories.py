from flask import url_for

from app.posts.entitys import Category


def test_category_view(client, auth_user):
    response = client.get(url_for("posts.categories"), follow_redirects=True)

    assert response.status_code == 200
    assert "Login" not in response.text
    assert "Categories" in response.text
    assert "Create category" in response.text


def test_category_page(client, auth_user, categories):
    response = client.get(url_for("posts.categories"), follow_redirects=True)

    assert response.status_code == 200

    for category in categories:
        assert category.name in response.text


def test_create_category(client, auth_user):
    response = client.post(url_for('posts.category_create'), data={
        'name': 'New Category'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Category successfully established' in response.text
    assert 'New Category' in response.text


def test_update_category(client, auth_user, init_db):
    response = client.post(url_for('posts.category_update', id=1), data={
        'name': 'Updated Category'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'You have successfully update a category' in response.text
    assert 'Updated Category' in response.text


def test_delete_category(client, auth_user, init_db):
    response = client.get(url_for('posts.category_delete', id=1), follow_redirects=True)

    assert response.status_code == 200
    assert 'Category successfully deleted' in response.text
    assert Category.query.get(1) is None
