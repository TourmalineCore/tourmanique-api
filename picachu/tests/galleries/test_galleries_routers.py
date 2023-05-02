import pytest
from flask import url_for


@pytest.mark.parametrize(
    'name',
    [
        ('Sliv Instasamki'),
        ('    Admin    '),
    ]
    )
def test_add_gallery_happy_path(name, flask_app, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        'name': name,
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)
    assert response.status_code == 201


@pytest.mark.parametrize(
    'name',
    [
        (''),
        ('   '),
    ]
    )
def test_add_gallery_unhappy_path(name, flask_app, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        'name': name,
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)
    assert response == 'Gallery name must not be empty.'
