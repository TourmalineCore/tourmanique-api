from http import HTTPStatus

from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from picachu.domain import Gallery
from picachu.modules.auth.is_user_has_access import IsUserHasAccess
from picachu.modules.galleries.commands.new_gallery_command import NewGalleryCommand

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
