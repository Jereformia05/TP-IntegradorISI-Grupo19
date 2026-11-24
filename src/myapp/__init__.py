from flask import Flask

import myapp.models  # noqa: F401
from myapp.api.health import health_bp
from myapp.config import Config
from myapp.extensions import db
from myapp.api.auth import auth_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registrar la ruta /health
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)

    return app
