from http import HTTPStatus

import pytest
from flask import url_for
from picachu.helpers.validate_json_helper import validate_json_schema
from pathlib import Path
import json

@pytest.mark.parametrize(
    'name',
    [
        ('Test Gallery'),
        ('    Admin    '),
        ('    Admin22    '),
        ('    Admin23    '),
    ]
    )
def test_add_gallery_with_correct_user_credentials(
        name,
        flask_app,
        db_without_test_data,
        access_token
):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        'name': name,
    }

    creation_response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)
    galleries = flask_app.get(url_for('api.galleries.get_galleries'), headers=headers)

    schema = json.loads(Path("./picachu/tests/galleries/data/galleries_schema.json").read_text())
    schema_validation_result = validate_json_schema(schema, galleries)

    assert creation_response.status_code == HTTPStatus.CREATED
    assert schema_validation_result is True


@pytest.mark.parametrize(
    'name',
    [
        (''),
        ('   '),
    ]
    )
def test_add_gallery_with_empty_user_credentials(
        name,
        flask_app,
        access_token
):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        'name': name,
    }

    response = flask_app.post(url_for('api.galleries.add_gallery'), json=data, headers=headers)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    ### No
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
