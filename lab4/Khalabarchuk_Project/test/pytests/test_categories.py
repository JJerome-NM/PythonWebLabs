from flask import url_for


def test_category_page(client, init_db, auth_user, categories):
    response = client.get(url_for("posts.categories"), follow_redirects=True)

    assert response.status_code == 200

    for category in categories:
        assert category.name in response.text
