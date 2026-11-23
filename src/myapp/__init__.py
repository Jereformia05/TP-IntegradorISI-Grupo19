from flask import Flask
from myapp.config import Config
from myapp.extensions import db
from myapp.api.health import health_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Registrar la ruta /health
    app.register_blueprint(health_bp)

    return app


