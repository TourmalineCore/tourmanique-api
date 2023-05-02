import pytest
from flask import url_for

from picachu.config.auth_config import auth_username, auth_password


def test_log_in_happy_path(flask_app):
    data = {
        'login': auth_username,
        'password': auth_password,
    }

    response = flask_app.post(url_for('api.auth.log_in'), json=data)

    assert response.status_code == 202


@pytest.mark.parametrize(
    'login, password',
    [
        ('Admin', 'admin'),
        ('ADMIN', 'ADMIN'),
        ('admin2', 'admin2'),
        ('', 'admin2'),
        ('', ''),
        ('admin2', ''),
    ]
    )
def test_log_in_unhappy_path(login, password, flask_app):
    data = {
        'login': login,
        'password': password,
    }

    response = flask_app.post(url_for('api.auth.log_in'), json=data)
    assert response.status_code == 401
