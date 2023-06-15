from http import HTTPStatus

import pytest
from flask import url_for

from tourmanique.config.auth_config import auth_username, auth_password
from tourmanique.helpers.validate_json_helper import validate_json_schema


def test_log_in_with_the_correct_user_credentials(flask_app):
    data = {
        'login': auth_username,
        'password': auth_password,
    }

    response = flask_app.post(url_for('api.auth.log_in'), json=data)

    schema = {
      "type": "object",
      "properties": {
        "accessToken": {
          "type": "object",
          "properties": {
            "value": {
              "type": "string"
            }
          },
          "required": [
            "value"
          ]
        }
      },
      "required": [
        "accessToken"
      ]
    }

    validate_response_schema = validate_json_schema(schema, response)

    assert validate_response_schema is True
    assert response.status_code == HTTPStatus.ACCEPTED


@pytest.mark.parametrize(
    'login, password',
    [
        ('admin', 'ADMIN'),
        ('admin2', 'admin'),
        ('admin2', 'admin2'),
    ]
    )
def test_log_in_with_the_incorrect_user_credentials(login, password, flask_app):
    data = {
        'login': login,
        'password': password,
    }

    response = flask_app.post(url_for('api.auth.log_in'), json=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.parametrize(
    'login, password',
    [
        ('admin', ''),
        ('', 'admin'),
        ('', ''),
    ]
    )
def test_log_in_with_empty_user_credentials(login, password, flask_app):
    data = {
        'login': login,
        'password': password,
    }

    response = flask_app.post(url_for('api.auth.log_in'), json=data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

