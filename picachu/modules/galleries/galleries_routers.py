from http import HTTPStatus

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from picachu.domain import Gallery
from picachu.modules.auth.is_user_has_access import IsUserHasAccess
from picachu.modules.galleries.commands.new_gallery_command import NewGalleryCommand

from picachu.domain.data_access_layer.session import session

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


@galleries_blueprint.route('/<gallery_id>/update-name', methods=['POST'])
@jwt_required()
def rename_gallery(gallery_id):
    current_user_id = get_jwt_identity()
    name_data = request.json.get('name')
    if not IsUserHasAccess().to_gallery(current_user_id):
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN

    gallery_entity = {
                      'name': name_data,
                      'user_id': current_user_id,
                      }

    try:
        gallery_entity = Gallery(**gallery_entity)
        gallery_name = NewGalleryCommand.rename(gallery_entity)
        return jsonify(gallery_name)

    except Exception as err:
        return jsonify(str(err)), HTTPStatus.BAD_REQUEST

# апдейт записи в базе данных