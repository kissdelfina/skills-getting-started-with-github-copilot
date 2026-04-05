import pytest

from src.app import activities


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    unknown_activity = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{unknown_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_requires_email_query_parameter(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup")

    # Assert
    assert response.status_code == 422


@pytest.mark.xfail(strict=True, reason="Known gap: no participant capacity enforcement in signup endpoint")
def test_signup_rejects_when_activity_is_full(client):
    # Arrange
    activity_name = "Chess Club"
    activity = activities[activity_name]

    while len(activity["participants"]) < activity["max_participants"]:
        activity["participants"].append(f"seed-{len(activity['participants'])}@mergington.edu")

    new_email = "overflow@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )

    # Assert
    assert response.status_code in (400, 409)
    assert new_email not in activities[activity_name]["participants"]


@pytest.mark.xfail(strict=True, reason="Known gap: no email format validation in signup endpoint")
def test_signup_rejects_invalid_email_format(client):
    # Arrange
    activity_name = "Chess Club"
    invalid_email = "not-an-email"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": invalid_email},
    )

    # Assert
    assert response.status_code == 422