from .application import app, setup_app


def test_home():
  setup_app(app)
  client = app.test_client()
  with app.test_request_context():

    response = client.get("/fr/")
    assert response.status_code == 200

    response = client.get("/fr/lieu/")
    assert response.status_code == 200

    response = client.get("/fr/programme/")
    assert response.status_code == 200

    response = client.get("/en/")
    assert response.status_code == 200
