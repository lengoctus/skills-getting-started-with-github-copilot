from urllib.parse import quote


def test_get_activities_returns_all_activities(client):
    """Arrange-Act-Assert: Test fetching all activities."""
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert isinstance(data[expected_activity]["participants"], list)


def test_signup_for_activity_adds_participant(client):
    """Arrange-Act-Assert: Test signing up a new participant."""
    # Arrange
    activity_name = "Chess Club"
    email = "test_student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"}

    # Verify participant was added
    activities_data = client.get("/activities").json()
    assert email in activities_data[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    """Arrange-Act-Assert: Test duplicate signup returns 400."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_participant_removes_participant(client):
    """Arrange-Act-Assert: Test unregistering a participant."""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants/{encoded_email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"}

    # Verify participant was removed
    activities_data = client.get("/activities").json()
    assert email not in activities_data[activity_name]["participants"]


def test_unregister_missing_participant_returns_404(client):
    """Arrange-Act-Assert: Test unregistering missing participant returns 404."""
    # Arrange
    activity_name = "Chess Club"
    email = "missing_student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")
    encoded_email = quote(email, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/participants/{encoded_email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
