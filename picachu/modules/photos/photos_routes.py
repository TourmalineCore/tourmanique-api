import io

import imagehash
from PIL import Image
from flask import Blueprint, request, jsonify

from picachu.config.rabbitmq_config import rabbitmq_photo_for_models_exchange_name
from picachu.domain import Photo
from picachu.helpers.rabbitmq_message_publisher.rabbitmq_message_publisher import RabbitMqMessagePublisher
from picachu.modules.photos.commands.new_photo_command import NewPhotoCommand
from picachu.helpers.s3_helper import S3Helper
from picachu.helpers.s3_paths import create_path_for_photo

photos_blueprint = Blueprint('photos', __name__, url_prefix='/photos')


@photos_blueprint.route('/add', methods=['POST'])
def add_photo():
    photo_bytes = request.get_data()

    photo_s3_path = create_path_for_photo()

    S3Helper().s3_upload_file(
        file_path_in_bucket=photo_s3_path,
        file_bytes=photo_bytes,
        public=True,
    )

    photo_hash = str(imagehash.average_hash(Image.open(io.BytesIO(photo_bytes))))
    photo_entity = Photo(photo_file_path_s3=photo_s3_path,
                         hash=photo_hash)
    photo_id = NewPhotoCommand().create(photo_entity)

    message_with_photo_parameters = {
        'photo_id': photo_id,
        'path_to_photo_in_s3': photo_s3_path,
    }

    RabbitMqMessagePublisher().publish_message_to_exchange(exchange_name=rabbitmq_photo_for_models_exchange_name,
                                                           message=message_with_photo_parameters)

    return jsonify(
        {'photo_id': photo_id}
    )
