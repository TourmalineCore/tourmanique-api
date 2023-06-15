from http import HTTPStatus

import pytest
from flask import url_for

from picachu.config.auth_config import auth_username, auth_password
from picachu.helpers.validate_json_helper import validate_json_schema
from pathlib import Path
import json


def test_successfully_authentication_if_all_params_are_valid(flask_app):
    user_authentication = {
        'login': auth_username,
        'password': auth_password,
    }

    authentication_response = flask_app.post(url_for('api.auth.log_in'), json=user_authentication)

    schema = json.loads(Path("./picachu/tests/auth/data/token_schema.json").read_text())
    schema_validation_result = validate_json_schema(schema, authentication_response)

    assert schema_validation_result is True
    assert authentication_response.status_code == HTTPStatus.ACCEPTED


@pytest.mark.parametrize(
    'login, password',
    [
        ('admin', 'ADMIN'),
        ('admin2', 'admin'),
        ('admin2', 'admin2'),
    ]
    )
def test_cant_authentication_if_invalid(login, password, flask_app):
    user_authentication = {
        'login': login,
        'password': password,
    }

    authentication_response = flask_app.post(url_for('api.auth.log_in'), json=user_authentication)
    assert authentication_response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    'login, password',
    [
        ('admin', ''),
        ('', 'admin'),
        ('', ''),
    ]
    )
def test_cant_authentication_if_empty(login, password, flask_app):
    user_authentication = {
        'login': login,
        'password': password,
    }

    authentication_response = flask_app.post(url_for('api.auth.log_in'), json=user_authentication)
    assert authentication_response.status_code == HTTPStatus.UNAUTHORIZED

