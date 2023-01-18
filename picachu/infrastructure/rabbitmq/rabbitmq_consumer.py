import json
import logging
import timeit
import traceback

from pika import BlockingConnection, ConnectionParameters, PlainCredentials
from pika.exceptions import ConnectionClosedByBroker, AMQPChannelError, AMQPConnectionError

from picachu.infrastructure.rabbitmq.rabbitmq_config_provider import RabbitMQConfigProvider

(
    rabbitmq_host,
    rabbitmq_username,
    rabbitmq_password,
) = RabbitMQConfigProvider.get_config()


class RabbitMqConsumer:
    def __init__(
            self,
            queue_name,
            consumption_handler,
    ):
        self.queue_name = queue_name
        self.consumption_handler = consumption_handler

    def run(self):
        logging.info('RabbitMQ consumer of queue={0} started'.format(self.queue_name))

        parameters = ConnectionParameters(
            host=rabbitmq_host,
            credentials=PlainCredentials(rabbitmq_username, rabbitmq_password),
            blocked_connection_timeout=300,
        )

        while True:
            try:
                logging.info('Connecting to RabbitMQ with host: {0}'.format(rabbitmq_host))
                connection = BlockingConnection(parameters)

                channel = connection.channel()
                channel.basic_qos(prefetch_count=1)

                channel.queue_declare(
                    queue=self.queue_name,
                    durable=True,
                    exclusive=False,
                    auto_delete=False,
                )

                channel.basic_consume(self.queue_name, self.on_message)

                # try:
                channel.start_consuming()
                # except KeyboardInterrupt:
                #     logging.info('Aborting...')
                #     channel.stop_consuming()
                #     connection.close()
                #     break

            except (ConnectionClosedByBroker, AMQPConnectionError):
                logging.info('Connection was closed, retrying...')
                continue

            except AMQPChannelError:
                logging.error('Caught a channel error: {0}, stopping...'.format(repr(traceback.format_exc())))
                break

            except Exception:
                logging.error('Unexpected error occurred: {0}'.format(repr(traceback.format_exc())))

    def on_message(self, channel, method_frame, header_frame, body):
        message_str = body.decode('utf-8')
        # ToDo need to escape because message is JSON object
        logging.info('Message Received {0}'.format(message_str))
        message = json.loads(message_str)

        try:
            start_processing = timeit.default_timer()
            self.consumption_handler(message)
            end_processing = timeit.default_timer()
            logging.info('Request processed for: ' + str(end_processing - start_processing) + 'secs')
        except Exception:
            logging.error('Unexpected error occurred: {0}'.format(repr(traceback.format_exc())))
            channel.basic_reject(delivery_tag=method_frame.delivery_tag, requeue=True)
            logging.info('Message rejected')
            return

        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        logging.info('Done (acknowledged)')
