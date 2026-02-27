"""
Tests for POST /activities/{activity_name}/signup endpoint using AAA (Arrange-Act-Assert) pattern.

This module tests the endpoint for signing up students to activities,
including success cases and error handling.
"""

import pytest


def test_signup_successful(client):
    """
    Test that a student can successfully sign up for an activity.
    
    AAA Pattern:
    - Arrange: Define activity name and email for a new signup
    - Act: Call the POST signup endpoint
    - Assert: Verify status code is 200 and response contains success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "newemail@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_adds_participant_to_activity(client):
    """
    Test that a participant is actually added to the activity after signup.
    
    AAA Pattern:
    - Arrange: Define activity name and email, get initial participant count
    - Act: Sign up the new participant, then retrieve all activities
    - Assert: Verify participant appears in the activity's participant list
    """
    # Arrange
    activity_name = "Programming Class"
    email = "test.student@mergington.edu"
    
    # Get initial state
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"].copy()
    
    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Get updated state
    updated_response = client.get("/activities")
    updated_participants = updated_response.json()[activity_name]["participants"]
    
    # Assert
    assert signup_response.status_code == 200
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_duplicate_email_returns_400(client):
    """
    Test that signing up with an email already in the activity returns 400 error.
    
    AAA Pattern:
    - Arrange: Choose an activity and an existing participant email
    - Act: Attempt to sign up with the same email twice
    - Assert: Verify second signup returns 400 status code and error message
    """
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"]


def test_signup_nonexistent_activity_returns_404(client):
    """
    Test that signing up for a non-existent activity returns 404 error.
    
    AAA Pattern:
    - Arrange: Define a non-existent activity name and a valid email
    - Act: Attempt to sign up for the non-existent activity
    - Assert: Verify response is 404 and contains error message
    """
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


def test_signup_multiple_students_same_activity(client):
    """
    Test that multiple different students can sign up for the same activity.
    
    AAA Pattern:
    - Arrange: Define activity name and create list of new emails
    - Act: Sign up each email for the activity
    - Assert: Verify all signups succeed and all are added to participants
    """
    # Arrange
    activity_name = "Art Studio"
    new_emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
    
    # Act
    responses = [
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        for email in new_emails
    ]
    
    # Get updated activity data
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    
    # Assert
    assert all(response.status_code == 200 for response in responses)
    assert all(email in participants for email in new_emails)
