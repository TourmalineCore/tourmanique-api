from http import HTTPStatus

import pytest
from flask import url_for
from picachu.helpers.validate_json_helper import validate_json_schema
from pathlib import Path
import json


@pytest.mark.parametrize(
    'gallery_name',
    [
        ('Test Gallery'),
        ('    Admin    '),
    ]
    )
def test_successfully_add_gallery_if_all_params_are_valid(
        gallery_name,
        flask_app,
        db_without_test_data,
        access_token
):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    gallery_creation_payload = {
        'name': gallery_name,
    }

    creation_response = flask_app.post(url_for('api.galleries.add_gallery'),
                                       json=gallery_creation_payload,
                                       headers=headers)
    galleries = flask_app.get(url_for('api.galleries.get_galleries'), headers=headers)

    schema = json.loads(Path("./picachu/tests/galleries/data/galleries_schema.json").read_text())
    schema_validation_result = validate_json_schema(schema, galleries)

    assert creation_response.status_code == HTTPStatus.CREATED
    assert schema_validation_result is True


@pytest.mark.parametrize(
    'gallery_name',
    [
        (''),
        ('   '),
    ]
    )
def test_cant_add_gallery_if_empty_or_whitespace_name(
        gallery_name,
        flask_app,
        access_token
):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    gallery_creation_payload = {
        'name': gallery_name,
    }

    creation_response = flask_app.post(url_for('api.galleries.add_gallery'),
                                       json=gallery_creation_payload,
                                       headers=headers)
    creation_error_message = json.loads(creation_response.text)['msg']

    assert creation_response.status_code == HTTPStatus.BAD_REQUEST
    assert creation_error_message == 'Gallery name must not be empty.'


@pytest.mark.parametrize(
    'invalid_access_token',
    [
        ("Bearer ''"),
        ("Bearer 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'"),
    ]
    )
def test_cant_add_gallery_if_invalid_access_token(invalid_access_token, flask_app):
    headers = {
        "Authorization": f'{invalid_access_token}'
    }

    gallery_creation_payload = {
        'name': 'gallery name',
    }

    creation_response = flask_app.post(url_for('api.galleries.add_gallery'),
                                       json=gallery_creation_payload,
                                       headers=headers)
    assert creation_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
