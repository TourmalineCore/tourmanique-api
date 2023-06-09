import datetime
from http import HTTPStatus

from flask import url_for
from flask_jwt_extended import create_access_token


def test_get_galleries(
        flask_app,
        db_with_test_data,
):
    header_token = create_access_token(identity=1,
                                       expires_delta=datetime.timedelta(days=30))

    response = flask_app.get(url_for("api.galleries.get_galleries"),
                             headers={"Authorization": f"Bearer {header_token}"})

    assert response.status_code == HTTPStatus.OK
    assert response.json == [
        {
            'id': 1,
            'name': 'gallery_1',
            'photosCount': 0,
            'previewPhotos': []
        },
        {
            'id': 2,
            'name': 'gallery_2',
            'photosCount': 0,
            'previewPhotos': []
        }
    ]
