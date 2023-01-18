import logging
from picachu.domain import Photo
from picachu.domain.dal import create_session
from picachu.infrastructure.rabbitmq.rabbitmq_config_provider import RabbitMQConfigProvider
from picachu.infrastructure.rabbitmq.rabbitmq_consumer import RabbitMqConsumer
from picachu.requests_consumer.commands.process_photo_request_command import ProcessPhotoRequestCommand


queue_name = RabbitMQConfigProvider.get_queue_names_config().rabbitmq_requests_queue_name


def process_model_request(message):
    current_session = create_session()
    try:
        result = ProcessPhotoRequestCommand(current_session).execute(message['path_to_image_in_s3'])

        if result:
            logging.warning('Created Photo ID: {0}'.format(result))

        current_session.commit()
    except Exception as e:
        logging.warning('Rollback session')
        current_session.rollback()
        raise
    finally:
        current_session.close()

    logging.warning(f'Message processed: {message["path_to_image_in_s3"]}')


if __name__ == '__main__':
    RabbitMqConsumer(
        queue_name,
        process_model_request,
    ).run()
