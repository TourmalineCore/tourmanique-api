import os

auth_username = os.getenv('AUTH_USERNAME')
auth_password = os.getenv('AUTH_PASSWORD')

if auth_username is None:
    raise ValueError('You should specify AUTH_USERNAME environment variable to be able to authenticate in service.')

if auth_password is None:
    raise ValueError('You should specify AUTH_PASSWORD environment variable to be able to authenticate in service.')
