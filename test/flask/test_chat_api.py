# Other modules
import pytest

# Local modules
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    return app

# todo(fxc)
