import json
import logging

import imagehash
import pika
from PIL import Image
from flask import Blueprint, request

from picachu.config import RabbitMQConfigProvider
from picachu.domain import Photo
from picachu.modules.photos.commands.new_photo_command import NewPhotoCommand
import io
from pika import ConnectionParameters, PlainCredentials
from picachu.helpers.s3_helper import S3Helper
from picachu.helpers.s3_paths import create_path_for_photo

photos_blueprint = Blueprint('photos', __name__, url_prefix='/photos')

(
    rabbitmq_host,
    rabbitmq_username,
    rabbitmq_password,
) = RabbitMQConfigProvider.get_config()

parameters = ConnectionParameters(
    host=rabbitmq_host,
    credentials=PlainCredentials(rabbitmq_username, rabbitmq_password),
)

exchange_name = RabbitMQConfigProvider.get_exchange_names_config().rabbitmq_requests_exchange_name

@photos_blueprint.route('/add', methods=['POST'])
def add_photo_and_photo_labels():
    photo_bytes = request.get_data()
    photo_s3_path = create_path_for_photo()

    photo_hash = str(imagehash.average_hash(Image.open(io.BytesIO(photo_bytes))))

    S3Helper().s3_upload_file(
        file_path_in_bucket=photo_s3_path,
        file_bytes=photo_bytes,
        public=True,
    )

    photo_entity = Photo(photo_file_path_s3=photo_s3_path,
                         hash=photo_hash)

    photo_id = NewPhotoCommand().create(photo_entity)

    value = {
        'photo_id': photo_id,
        'path_to_photo_in_s3': photo_s3_path,
    }

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host,
                credentials=pika.credentials.PlainCredentials(rabbitmq_username, rabbitmq_password)
            )
        )
        channel = connection.channel()

        logging.warning('RabbitMQ exchange declaration {0}'.format(exchange_name))
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

        body_str = json.dumps(value)
        body = body_str.encode('utf-8')
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='',  # ignored by fanout exchange type
            body=body,
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            )
        )

        logging.warning('Model request sent: {0}'.format(body_str))
    except Exception:
        logging.warning('Aborting...')
        connection.close()

    return {
        'photo_id': photo_id
    }
