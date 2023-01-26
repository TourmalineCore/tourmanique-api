import json
import logging

import imagehash
import pika
from PIL import Image
from flask import Blueprint, request, jsonify

from picachu.config import rabbitmq_photo_for_models_exchange_name, rabbitmq_host, rabbitmq_username, rabbitmq_password
from picachu.domain import Photo
from picachu.modules.photos.commands.new_photo_command import NewPhotoCommand
import io
from pika import ConnectionParameters, PlainCredentials
from picachu.helpers.s3_helper import S3Helper
from picachu.helpers.s3_paths import create_path_for_photo

photos_blueprint = Blueprint('photos', __name__, url_prefix='/photos')

PARAMETERS = ConnectionParameters(
    host=rabbitmq_host,
    credentials=PlainCredentials(rabbitmq_username, rabbitmq_password),
)

EXCHANGE_NAME = rabbitmq_photo_for_models_exchange_name


@photos_blueprint.route('/add', methods=['POST'])
def add_photo_and_photo_labels():
    photo_bytes = request.get_data()

    photo_s3_path = create_path_for_photo()
    photo_hash = str(imagehash.average_hash(Image.open(io.BytesIO(photo_bytes))))

    photo_entity = Photo(photo_file_path_s3=photo_s3_path,
                         hash=photo_hash)

    S3Helper().s3_upload_file(
        file_path_in_bucket=photo_s3_path,
        file_bytes=photo_bytes,
        public=True,
    )

    photo_id = NewPhotoCommand().create(photo_entity)

    message_with_photo_parameters = {
        'photo_id': photo_id,
        'path_to_photo_in_s3': photo_s3_path,
    }

    connection = pika.BlockingConnection(PARAMETERS)
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='fanout')
    logging.warning('Exchange declared {0}'.format(EXCHANGE_NAME))

    try:
        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key='',  # ignored by fanout exchange type
            body=json.dumps(message_with_photo_parameters).encode('utf-8'),
            properties=pika.BasicProperties(
                delivery_mode=2,
            )
        )

        logging.warning('Model request sent: {0}'.format(message_with_photo_parameters))
    except Exception:
        logging.warning('Aborting...')
        connection.close()

    return jsonify({'photo_id': photo_id})
