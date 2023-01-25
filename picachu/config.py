"""Сonfiguration
Use env var to override
"""
import os

ENV = os.getenv('FLASK_ENV')
DEBUG = ENV == 'development'

s3_endpoint = os.getenv('S3_ENDPOINT')
if s3_endpoint is None:
    raise ValueError('You should specify S3_ENDPOINT environment variable to be able to connect to S3 bucket.')

s3_access_key_id = os.getenv('S3_ACCESS_KEY_ID')
if s3_access_key_id is None:
    raise ValueError('You should specify S3_ACCESS_KEY_ID environment variable to be able to connect to S3 bucket.')

s3_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
if s3_secret_access_key is None:
    raise ValueError('You should specify S3_SECRET_ACCESS_KEY environment variable to be able to connect to S3 bucket.')

s3_bucket_name = os.getenv('S3_BUCKET_NAME')
if s3_bucket_name is None:
    raise ValueError('You should specify S3_BUCKET_NAME environment variable to be able to connect to S3 bucket.')

s3_prefix = os.getenv('S3_PREFIX', default='')

s3_use_ssl = os.getenv('S3_USE_SSL', default='true').lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup']

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_username = os.getenv('RABBITMQ_DEFAULT_USER')
rabbitmq_password = os.getenv('RABBITMQ_DEFAULT_PASS')

rabbitmq_requests_exchange_name = os.getenv('RABBITMQ_REQUESTS_EXCHANGE_NAME')

if not rabbitmq_host:
    raise ValueError('You should specify RABBITMQ_HOST to be able to connect to RabbitMQ.')

if not rabbitmq_username:
    raise ValueError('You should specify RABBITMQ_DEFAULT_USER to be able to connect to RabbitMQ.')

if not rabbitmq_password:
    raise ValueError('You should specify RABBITMQ_DEFAULT_PASS to be able to connect to RabbitMQ.')

if not rabbitmq_requests_exchange_name:
    raise ValueError('You should specify RABBITMQ_REQUESTS_EXCHANGE_NAME to be able to connect to requests exchange.')

class ExchangeNamesConfig:
    def __init__(self):
        self.rabbitmq_requests_exchange_name = rabbitmq_requests_exchange_name


class RabbitMQConfigProvider:
    @staticmethod
    def get_config():
        return (
            rabbitmq_host,
            rabbitmq_username,
            rabbitmq_password,
        )

    @staticmethod
    def get_exchange_names_config():
        return ExchangeNamesConfig()

