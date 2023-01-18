import logging

from PIL.Image import Image
from flask import Blueprint, request
from picachu.modules.photos.photo_preprocessing import preprocess_photo
from pika import ConnectionParameters, PlainCredentials, BlockingConnection, BasicProperties
from picachu.helpers.s3_helper import S3Helper
from picachu.helpers.s3_paths import create_path_for_photo
from picachu.infrastructure.rabbitmq.rabbitmq_config_provider import RabbitMQConfigProvider

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

requests_queue_name = RabbitMQConfigProvider().get_queue_names_config().rabbitmq_requests_queue_name


@photos_blueprint.route('/add', methods=['POST'])
def add_photo_and_photo_labels():
    photo_bytes = request.get_data()
    photo_s3_path = create_path_for_photo()

    S3Helper().s3_upload_file(
        file_path_in_bucket=photo_s3_path,
        file_bytes=photo_bytes,
        public=True,
    )

    connection = BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=requests_queue_name, durable=True)

    try:
        print('{"path_to_image_in_s3": "' + str(photo_s3_path) + '"}')
        channel.basic_publish(
            exchange='',
            routing_key=requests_queue_name,
            body='{"path_to_image_in_s3": "' + str(photo_s3_path) + '"}',
            properties=BasicProperties(
                delivery_mode=2,
            )
        )
        logging.warning(f'Message with path: {photo_s3_path} published')

    except Exception:
        logging.warning('Aborting...')
        connection.close()

    return {
        'photo_s3_path': photo_s3_path
    }
