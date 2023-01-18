import os

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_username = os.getenv('RABBITMQ_DEFAULT_USER')
rabbitmq_password = os.getenv('RABBITMQ_DEFAULT_PASS')

rabbitmq_requests_exchange_name = os.getenv('RABBITMQ_REQUESTS_EXCHANGE_NAME')
rabbitmq_requests_queue_name = os.getenv('RABBITMQ_REQUESTS_QUEUE_NAME')
rabbitmq_results_queue_name = os.getenv('RABBITMQ_RESULTS_QUEUE_NAME')

if not rabbitmq_host:
    raise ValueError('You should specify RABBITMQ_HOST to be able to connect to RabbitMQ.')

if not rabbitmq_username:
    raise ValueError('You should specify RABBITMQ_DEFAULT_USER to be able to connect to RabbitMQ.')

if not rabbitmq_password:
    raise ValueError('You should specify RABBITMQ_DEFAULT_PASS to be able to connect to RabbitMQ.')

if not rabbitmq_requests_exchange_name:
    raise ValueError('You should specify RABBITMQ_REQUESTS_EXCHANGE_NAME to be able to connect to requests exchange.')

if not rabbitmq_requests_queue_name:
    raise ValueError('You should specify RABBITMQ_REQUESTS_QUEUE_NAME to be able to connect to queue with requests.')

if not rabbitmq_results_queue_name:
    raise ValueError('You should specify RABBITMQ_RESULTS_QUEUE_NAME to be able to connect to results queue.')


class ExchangeNamesConfig:
    def __init__(self):
        self.rabbitmq_requests_exchange_name = rabbitmq_requests_exchange_name


class QueueNamesConfig:
    def __init__(self):
        self.rabbitmq_requests_queue_name = rabbitmq_requests_queue_name
        self.rabbitmq_results_queue_name = rabbitmq_results_queue_name


class RabbitMQConfigProvider:
    @staticmethod
    def get_config():
        return (
            rabbitmq_host,
            rabbitmq_username,
            rabbitmq_password,
        )

    @staticmethod
    def get_queue_names_config():
        return QueueNamesConfig()

    @staticmethod
    def get_exchange_names_config():
        return ExchangeNamesConfig()
