from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from picachu.domain import Gallery

from picachu.modules.auth.is_user_has_access import IsUserHasAccess

from picachu.modules.galleries.commands.delete_gallery_command import DeleteGalleryCommand
from picachu.modules.galleries.commands.new_gallery_command import NewGalleryCommand
from picachu.modules.galleries.commands.update_gallery_command import UpdateGalleryCommand

from picachu.modules.galleries.queries.get_gallery_query import GetGalleryQuery

from picachu.modules.photos.queries.get_photos_query import GetPhotoQuery

galleries_blueprint = Blueprint('galleries', __name__, url_prefix='/galleries')


@galleries_blueprint.route('/', methods=['POST'])
@jwt_required()
def add_gallery():
    current_user_id = get_jwt_identity()
    if not IsUserHasAccess().to_service(current_user_id):
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    gallery_entity = {
                      'name': 'new gallery',
                      'user_id': current_user_id,
                      }

    try:
        gallery_entity = Gallery(**gallery_entity)
        gallery_id = NewGalleryCommand.create(gallery_entity)

        return jsonify(gallery_id), HTTPStatus.CREATED

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@galleries_blueprint.route('/<int:gallery_id>/rename', methods=['POST'])
@jwt_required()
def rename_gallery(gallery_id):
    current_user_id = get_jwt_identity()
    new_gallery_name = request.json.get('name')
    if not IsUserHasAccess.to_gallery(current_user_id, gallery_id):
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN
    if not GetGalleryQuery.by_id(gallery_id):
        return jsonify({'msg': 'Not Found'}), HTTPStatus.NOT_FOUND
    try:
        UpdateGalleryCommand().rename(new_gallery_name, gallery_id)
        return jsonify({'msg': 'OK'}), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@galleries_blueprint.route('/<int:gallery_id>/', methods=['DELETE'])
@jwt_required()
def delete_gallery(gallery_id):
    current_user_id = get_jwt_identity()
    if not IsUserHasAccess.to_gallery(current_user_id, gallery_id):
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN
    if not GetGalleryQuery.by_id(gallery_id):
        return jsonify({'msg': 'Not Found'}), HTTPStatus.NOT_FOUND
    try:
        DeleteGalleryCommand().delete(gallery_id)
        return jsonify(gallery_id), HTTPStatus.OK

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST


@galleries_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_galleries():
    current_user_id = get_jwt_identity()
    if not IsUserHasAccess.to_service(current_user_id):
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN
    try:
        galleries_list = GetGalleryQuery().by_user_id(current_user_id)
        result = []
        for gallery in galleries_list:
            result.append({'id': gallery.id,
                           'name': gallery.name,
                           'photosCount': GetPhotoQuery.count_photos(gallery.id)})
        return jsonify(result), HTTPStatus.OK
    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST
