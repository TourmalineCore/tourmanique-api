import io
from http import HTTPStatus

import imagehash
from PIL import Image
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from picachu.config.rabbitmq_config import rabbitmq_photo_for_models_exchange_name
from picachu.domain import Photo
from picachu.helpers.rabbitmq_message_publisher.rabbitmq_message_publisher import RabbitMqMessagePublisher
from picachu.modules.auth.is_user_has_access import IsUserHasAccess
from picachu.modules.galleries.queries.get_gallery_query import GetGalleryQuery
from picachu.modules.photos.commands.new_photo_command import NewPhotoCommand
from picachu.helpers.s3_helper import S3Helper
from picachu.helpers.s3_paths import create_path_for_photo

photos_blueprint = Blueprint('photos', __name__, url_prefix='/photos')


@photos_blueprint.route('/<int:gallery_id>/upload-photo', methods=['POST'])
@jwt_required()
def add_photo(gallery_id):
    photo_bytes = request.get_data()
    current_user_id = get_jwt_identity()
    if not IsUserHasAccess.to_gallery(current_user_id):
        return jsonify({'msg': 'Forbidden'}), HTTPStatus.FORBIDDEN
    if not GetGalleryQuery.by_id(gallery_id):
        return jsonify({'msg': 'Not Found'}), HTTPStatus.NotFound

    photo_s3_path = create_path_for_photo()

    S3Helper().s3_upload_file(
        file_path_in_bucket=photo_s3_path,
        file_bytes=photo_bytes,
        public=True,
    )

    photo_hash = str(imagehash.average_hash(Image.open(io.BytesIO(photo_bytes))))
    photo_entity = Photo(photo_file_path_s3=photo_s3_path,
                         hash=photo_hash,
                         gallery_id=gallery_id)
    photo_id = NewPhotoCommand().create(photo_entity)

    message_with_photo_parameters = {
        'photo_id': photo_id,
        'path_to_photo_in_s3': photo_s3_path,
    }

    RabbitMqMessagePublisher().publish_message_to_exchange(exchange_name=rabbitmq_photo_for_models_exchange_name,
                                                           message=message_with_photo_parameters)

    return jsonify({'msg': 'OK'}), HTTPStatus.OK
