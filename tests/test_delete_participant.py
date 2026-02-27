"""
Tests for DELETE /activities/{activity_name}/participants endpoint using AAA (Arrange-Act-Assert) pattern.

This module tests the endpoint for removing students from activities,
including success cases and error handling.
"""

import pytest


def test_delete_removes_participant(client):
    """
    Test that a participant is successfully removed from an activity.
    
    AAA Pattern:
    - Arrange: Choose an activity and get an existing participant
    - Act: Call the DELETE endpoint to remove the participant
    - Assert: Verify status code is 200 and response contains success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Existing participant
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_delete_removes_from_participants_list(client):
    """
    Test that the participant is actually removed from the activity's participant list.
    
    AAA Pattern:
    - Arrange: Choose an activity and participant, get initial participant count
    - Act: Delete the participant and retrieve updated activity data
    - Assert: Verify participant is no longer in the list and count decreased by 1
    """
    # Arrange
    activity_name = "Drama Club"
    email = "ava@mergington.edu"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"].copy()
    initial_count = len(initial_participants)
    
    # Act
    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Get updated state
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    
    # Assert
    assert delete_response.status_code == 200
    assert email not in updated_participants
    assert len(updated_participants) == initial_count - 1


def test_delete_nonexistent_activity_returns_404(client):
    """
    Test that deleting from a non-existent activity returns 404 error.
    
    AAA Pattern:
    - Arrange: Define a non-existent activity name and a valid email
    - Act: Attempt to delete from the non-existent activity
    - Assert: Verify response is 404 and contains error message
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_delete_nonexistent_participant_returns_404(client):
    """
    Test that deleting a participant not in the activity returns 404 error.
    
    AAA Pattern:
    - Arrange: Choose an activity and an email not in its participants
    - Act: Attempt to delete the non-existent participant
    - Assert: Verify response is 404 and contains error message
    """
    # Arrange
    activity_name = "Basketball Team"
    non_existent_email = "notinclub@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": non_existent_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_delete_multiple_participants(client):
    """
    Test that multiple participants can be removed from the same activity.
    
    AAA Pattern:
    - Arrange: Choose an activity and multiple participants to remove
    - Act: Delete each participant sequentially
    - Assert: Verify all deletions succeed and all are removed from participants list
    """
    # Arrange
    activity_name = "Debate Team"
    emails_to_remove = ["liam@mergington.edu", "lucas@mergington.edu"]
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"].copy()
    
    # Act
    responses = [
        client.delete(
            f"/activities/{activity_name}/participants",
            params={"email": email}
        )
        for email in emails_to_remove
    ]
    
    # Get updated state
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    
    # Assert
    assert all(response.status_code == 200 for response in responses)
    assert all(email not in updated_participants for email in emails_to_remove)
    assert len(updated_participants) == len(initial_participants) - 2


def test_delete_then_readd_participant(client):
    """
    Test that a participant can be removed and then added back to an activity.
    
    AAA Pattern:
    - Arrange: Choose an activity and participant to remove/re-add
    - Act: Delete the participant, then sign them up again
    - Assert: Verify both operations succeed and participant is in the list
    """
    # Arrange
    activity_name = "Tennis Club"
    email = "noah@mergington.edu"
    
    # Act - Delete
    delete_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Verify deletion
    check_after_delete = client.get("/activities")
    participants_after_delete = check_after_delete.json()[activity_name]["participants"]
    
    # Act - Re-add
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Verify re-addition
    check_after_signup = client.get("/activities")
    participants_after_signup = check_after_signup.json()[activity_name]["participants"]
    
    # Assert
    assert delete_response.status_code == 200
    assert email not in participants_after_delete
    assert signup_response.status_code == 200
    assert email in participants_after_signup
