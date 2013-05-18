from .main import app


def test_home():
  client = app.test_client()
  with app.test_request_context():
    response = client.get("/")
    assert response.status_code == 200
