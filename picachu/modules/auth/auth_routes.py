import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

USER_ID = 1

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/login', methods=['POST'])
def log_in():
    user_data = request.json.get('login')
    password_data = request.json.get('password')

    if user_data != 'admin' or password_data != 'admin':
        return jsonify({'msg': 'Bad username or password'}), 401

    access_token = create_access_token(identity=USER_ID,
                                       expires_delta=datetime.timedelta(days=30))

    return jsonify({
        "accessToken": {
            "value": access_token
        },
    })
