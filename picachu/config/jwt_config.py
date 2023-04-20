import os

jwt_secret_key = os.getenv('JWT_SECRET_KEY')

if jwt_secret_key is None:
    raise ValueError('You must specify the JWT_SECRET_KEY environment variable to be able to use JWT in the project.')
