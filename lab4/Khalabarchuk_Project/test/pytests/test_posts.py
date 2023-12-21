from flask import url_for

from app.posts.entitys import Post, PostType, Category


def test_all_post_view(client, auth_user):
    response = client.get(url_for('posts.all_posts'), follow_redirects=True)

    assert response.status_code == 200
    assert 'Posts' in response.text
    assert 'Create post' in response.text
    assert f'<form action="{url_for("posts.all_posts")}' in response.text


def test_post_create_view(client, auth_user):
    response = client.get(url_for('posts.create_post'), follow_redirects=True)

    assert response.status_code == 200
    assert 'Create post' in response.text
    assert f'<form action="{url_for("posts.create_post")}' in response.text


def test_post_by_id_view(client, auth_user, init_db):
    post: Post = Post.query.get(1)
    response = client.get(url_for('posts.get_post', id=1), follow_redirects=True)

    assert response.status_code == 200

    if post.user_id == auth_user.id:
        assert f'<a href="{url_for('posts.update_post', id=1)}">' in response.text
        assert f'<a href="{url_for('posts.delete_post', id=1)}">' in response.text
    else:
        assert f'<a href="{url_for('posts.update_post', id=1)}">' not in response.text
        assert f'<a href="{url_for('posts.delete_post', id=1)}">' not in response.text

    assert str(post.created) in response.text


def test_post_edit_view(client, auth_user):
    response = client.get(url_for('posts.update_post', id=1), follow_redirects=True)

    assert response.status_code == 200
    assert 'Edit post' in response.text
    assert f'<form action="{url_for("posts.update_post", id=1)}' in response.text


def test_create_post(client, auth_user):
    response = client.post(url_for('posts.create_post'), data={
        'title': 'Test Post',
        'text': 'This is a test post content',
        'category': '1'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert 'Test Post' in response.text
    assert 'This is a test post content' in response.text


def test_update_post(client, auth_user, init_db):
    old_post: Post = Post.query.first()

    data = {
        "title": "New best title",
        "text": "Very coool text",
        "image": old_post.image,
        "type": PostType.OTHER.name,
        "category": Category.query.get(1).id,
        "tags": [tag.name for tag in old_post.tags],
        "enable": old_post.enable
    }

    response = client.post(url_for('posts.update_post', id=old_post.id), data=data, follow_redirects=True)

    assert response.status_code == 200

    post: Post = Post.query.get(old_post.id)

    assert post.title == data["title"]
    assert post.text == data["text"]
    assert post.category.id == data["category"]


def test_delete_post(client, auth_user, init_db):
    post: Post = Post.query.first()
    response = client.get(url_for('posts.delete_post', id=post.id), follow_redirects=True)

    assert response.status_code == 200
    assert 'Post successfully deleted' in response.text
    assert Post.query.get(post.id) is None
