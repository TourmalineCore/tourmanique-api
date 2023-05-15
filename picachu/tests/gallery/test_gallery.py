import datetime
from http import HTTPStatus

from flask import url_for
from sqlalchemy import select
from picachu.domain import Gallery
from flask_jwt_extended import create_access_token


def test_get_galleries(db_session, create_test_data):

    with db_session() as session:
        query_result = session.execute(select(Gallery)).all()

    assert 'dmwdmwe' in str(query_result)


# def test_get_galleries_from_endpoint(flask_app, create_test_data):
#     header_token = create_access_token(identity=1,
#                                        expires_delta=datetime.timedelta(days=30))
#     response = flask_app.get(url_for("api.galleries.get_galleries"),
#                              headers={"Authorization": f"Bearer {header_token}"})
#
#     assert response.status_code == HTTPStatus.OK
#     assert response.json == ',cm'
