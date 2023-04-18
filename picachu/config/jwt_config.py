import os

jwt_secret_token = os.getenv('JWT_SECRET_KEY')

if jwt_secret_token is None:
    raise ValueError('You should specify JWT_SECRET_KEY environment variable to be able to connect to JWT.')