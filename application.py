from flask import Flask, Blueprint
from flask_cors import CORS
from flask_migrate import upgrade as _upgrade

from picachu.domain.dal import db, migrate, build_connection_string
from picachu.modules.labels.labels_routes import labels_blueprint
from picachu.modules.photos.photos_routes import photos_blueprint


def create_app():
    """Application factory, used to create application"""
    app = Flask(__name__)
    app.config.from_object('picachu.config')

    # without this /feeds will work but /feeds/ with the slash at the end won't
    app.url_map.strict_slashes = False

    # allow to call the api from any origin for now
    CORS(
        app,
    )

    app.config['SQLALCHEMY_DATABASE_URI'] = build_connection_string()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    register_blueprints(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # runs pending migrations
    with app.app_context():
        _upgrade()

    return app


def register_blueprints(app):
    """Register all blueprints for application"""
    api_blueprint = Blueprint('api', __name__, url_prefix='/api')
    api_blueprint.register_blueprint(labels_blueprint)
    api_blueprint.register_blueprint(photos_blueprint)

    app.register_blueprint(api_blueprint)
