from .application import app, setup_app
from .extensions import db


class TestConfig(object):
  SQLALCHEMY_DATABASE_URI = "sqlite://"


def test_home():
  setup_app(app, TestConfig())
  client = app.test_client()
  with app.test_request_context():
    db.create_all()

    response = client.get("/fr/")
    assert response.status_code == 200

    response = client.get("/fr/lieu/")
    assert response.status_code == 200

    response = client.get("/fr/programme/")
    assert response.status_code == 200

    response = client.get("/fr/registration/")
    assert response.status_code == 200

    response = client.get("/fr/participants/")
    assert response.status_code == 200

    response = client.get("/en/")
    assert response.status_code == 200
