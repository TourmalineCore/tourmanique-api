"""Сonfiguration
Use env var to override
"""
import os

ENV = os.getenv('FLASK_ENV')
DEBUG = ENV == 'development'

s3_endpoint = os.getenv('S3_ENDPOINT')
s3_access_key_id = os.getenv('S3_ACCESS_KEY_ID')
s3_secret_access_key = os.getenv('S3_SECRET_ACCESS_KEY')
s3_bucket_name = os.getenv('S3_BUCKET_NAME')
s3_prefix = os.getenv('S3_PREFIX', default='')
s3_use_ssl = os.getenv('S3_USE_SSL', default='true').lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup']

if s3_endpoint is None:
    raise ValueError('You should specify S3_ENDPOINT environment variable to be able to connect to S3 bucket.')
if s3_access_key_id is None:
    raise ValueError('You should specify S3_ACCESS_KEY_ID environment variable to be able to connect to S3 bucket.')
if s3_secret_access_key is None:
    raise ValueError('You should specify S3_SECRET_ACCESS_KEY environment variable to be able to connect to S3 bucket.')
if s3_bucket_name is None:
    raise ValueError('You should specify S3_BUCKET_NAME environment variable to be able to connect to S3 bucket.')


rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_username = os.getenv('RABBITMQ_DEFAULT_USER')
rabbitmq_password = os.getenv('RABBITMQ_DEFAULT_PASS')

if rabbitmq_host is None:
    raise ValueError('You should specify RABBITMQ_HOST to be able to connect to RabbitMQ.')
if rabbitmq_username is None:
    raise ValueError('You should specify RABBITMQ_DEFAULT_USER to be able to connect to RabbitMQ.')
if rabbitmq_password is None:
    raise ValueError('You should specify RABBITMQ_DEFAULT_PASS to be able to connect to RabbitMQ.')


rabbitmq_photo_for_models_exchange_name = os.getenv('RABBITMQ_PHOTO_FOR_MODELS_EXCHANGE_NAME')
if rabbitmq_photo_for_models_exchange_name is None:
    raise ValueError('You should specify RABBITMQ_PHOTO_FOR_MODELS_EXCHANGE_NAME to be able to connect to exchange.')
