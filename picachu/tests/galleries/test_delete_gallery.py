from http import HTTPStatus

import pytest
from flask import url_for


def test_delete_gallery(flask_app, add_gallery):
    """Test removing gallery"""
    response = flask_app.delete(url_for('api.galleries.delete_gallery'))
    assert response.status_code == HTTPStatus.OK
