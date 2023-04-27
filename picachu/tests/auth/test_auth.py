import pytest
from flask import url_for

from picachu.config.auth_config import auth_username, auth_password


@pytest.mark.parametrize(
    'login, password, valid',
    [
        (auth_username, auth_password, True),
        ('Admin', 'admin', False),
        ('ADMIN', 'ADMIN', False),
        ('admin2', 'admin2', False),
        ('', 'admin2', False),
        ('', '', False),
        ('admin2', '', False),
    ]
    )
def test_log_in(login, password, valid, flask_app):
    data = {
        'login': login,
        'password': password,
    }

    response = flask_app.post(url_for('api.auth.log_in'), json=data)

    if valid:
        assert response.status_code == 202
    else:
        assert response.status_code == 401

