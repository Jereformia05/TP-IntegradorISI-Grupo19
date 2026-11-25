from flask import Flask

import myapp.models  # noqa: F401
from myapp.api.answers import answers_bp
from myapp.api.auth import auth_bp
from myapp.api.classification import classification_bp
from myapp.api.health import health_bp
from myapp.config import Config
from myapp.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(answers_bp)
    app.register_blueprint(classification_bp)
    return app