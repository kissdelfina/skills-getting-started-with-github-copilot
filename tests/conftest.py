from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app

INITIAL_ACTIVITIES_STATE = deepcopy(activities)


def restore_activities_state():
    """Reset in-memory activity data to baseline for deterministic tests."""
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES_STATE))


@pytest.fixture(autouse=True)
def reset_activities_state():
    # Arrange shared baseline before each test and clean up after.
    restore_activities_state()
    yield
    restore_activities_state()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client