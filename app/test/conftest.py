import pytest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import create_app

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.debug = True
    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()
    # Get Reference to client object
    # In order to perform tests
    yield app
    # Clean up
    # Teardown
    # Close Database Connection
    # ETC
    ctx.pop()
