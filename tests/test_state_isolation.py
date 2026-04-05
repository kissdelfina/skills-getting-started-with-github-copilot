from src.app import activities
from tests.conftest import restore_activities_state


def test_restore_activities_state_resets_mutated_data():
    # Arrange
    activity_name = "Chess Club"
    marker_email = "temporary-marker@mergington.edu"
    activities[activity_name]["participants"].append(marker_email)
    assert marker_email in activities[activity_name]["participants"]

    # Act
    restore_activities_state()

    # Assert
    assert marker_email not in activities[activity_name]["participants"]