import pytest
from app import create_app
from app.config import TestConfig

# from app.models import Users


@pytest.fixture(scope="module")
def test_client():
    # Set up a test client using the TestConfig
    flask_app = create_app(TestConfig)

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  # Yield the test client to the test functions