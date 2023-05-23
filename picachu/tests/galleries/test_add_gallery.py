from http import HTTPStatus

import pytest
from flask import url_for


@pytest.mark.parametrize(
    'name',
    [
        ('Test Gallery'),
        ('    Admin    '),
    ]
    )
def test_add_gallery_with_correct_user_credentials(name, flask_app, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        'name': name,
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize(
    'name',
    [
        (''),
        ('   '),
    ]
    )
def test_add_gallery_with_empty_user_credentials(name, flask_app, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        'name': name,
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.text == '{\n  "msg": "Gallery name must not be empty."\n}\n'


def test_add_gallery_with_incorrect_token(flask_app):
    headers = {
        "Authorization": f"Bearer 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'"
    }

    data = {
        'name': 'Test Gallery2',
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_add_gallery_with_empty_token(flask_app):
    headers = {
        "Authorization": f"Bearer ''"
    }

    data = {
        'name': 'Test Gallery3',
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
