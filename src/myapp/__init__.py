from flask import Flask

import myapp.models  # noqa: F401
from myapp.api.agent import agent_bp
from myapp.api.answers import answers_bp
from myapp.api.auth import auth_bp
from myapp.api.classification import classification_bp
from myapp.api.health import health_bp
from myapp.api.questions import questions_bp
from myapp.config import Config
from myapp.extensions import db
from myapp.views.web import web_bp


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(config_class)

    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = "dev-secret-key-123"
    
    
    db.init_app(app)

    # Registrar blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(answers_bp)
    app.register_blueprint(classification_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(agent_bp)
    app.register_blueprint(web_bp)
    
    return app
