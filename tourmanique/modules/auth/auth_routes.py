import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from tourmanique.config.auth_config import auth_username, auth_password
from http import HTTPStatus

USER_ID = 1

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/login', methods=['POST'])
def log_in():
    user_data = request.json.get('login')
    password_data = request.json.get('password')

    if user_data != auth_username or password_data != auth_password:
        return jsonify({'msg': 'Bad username or password'}), HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=USER_ID,
                                       expires_delta=datetime.timedelta(days=30))

    return jsonify({
        "accessToken": {
            "value": access_token
        }
    }), HTTPStatus.ACCEPTED
