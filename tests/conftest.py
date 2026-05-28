import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def preserve_activities():
    """Fixture to preserve and restore activities state between tests."""
    original_activities = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client():
    """Fixture to provide a TestClient for API tests."""
    return TestClient(app)
