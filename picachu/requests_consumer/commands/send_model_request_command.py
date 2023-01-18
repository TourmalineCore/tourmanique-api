import json
import logging
import traceback

import pika

from picachu.infrastructure.rabbitmq.rabbitmq_config_provider import RabbitMQConfigProvider

(
    rabbitmq_host,
    rabbitmq_username,
    rabbitmq_password,
) = RabbitMQConfigProvider.get_config()

exchange_name = RabbitMQConfigProvider.get_exchange_names_config().rabbitmq_requests_exchange_name


class SendModelRequestCommand:
    def __init__(self, failed_callback=None):
        self.failed_callback = failed_callback

    def _execute(self, value):
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
        except Exception as e:
            logging.error('Unexpected error occurred: {0}'.format(repr(traceback.format_exc())))

            if self.failed_callback:
                self.failed_callback()

            raise

    def execute(
            self,
            photo_id,
            path_to_photo_in_s3,
    ):

        value = {
            'photo_id': photo_id,
            'path_to_photo_in_s3': path_to_photo_in_s3,
        }

        self._execute(value)

    def resend(self, deserialized_message: str):
        self._execute(deserialized_message)
