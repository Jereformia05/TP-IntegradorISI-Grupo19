import pytest 
from myapp import create_app
from myapp.extensions import db
import myapp.models # Importante: carga User, Question, Answer en SQLAlchemy

@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()
