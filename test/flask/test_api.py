# Other modules
import pytest

# Local modules
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app


def test_api_bad_request(app):
    with app.test_client() as client:
        response = client.get("/v1/tests/bad-request")
        assert response.status_code == 400
        assert response.json["status"] == "error"
        assert response.json["message"] == "Bad Request"


def test_api_forbidden(app):
    with app.test_client() as client:
        response = client.get("/v1/tests/forbidden")
        assert response.status_code == 403
        assert response.json["status"] == "error"
        assert (
                response.json["message"]
                == "You don't have the permission to access the requested resource"
        )


def test_api_internal_server_error(app):
    with app.test_client() as client:
        response = client.get("/v1/tests/internal-server-error")
        assert response.status_code == 500
        assert response.json["status"] == "error"
        assert response.json["message"] == "Internal Server Error"


def test_api_unknown_exception(app):
    with app.test_client() as client:
        response = client.get("/v1/tests/unknown-exception")
        assert response.status_code == 500
        assert response.json["status"] == "error"
        assert response.json["message"] == "Internal Server Error"


def test_api_login(app):
    # todo(fxc)
    # ping after login
    pass
