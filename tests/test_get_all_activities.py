"""
Tests for GET /activities endpoint using AAA (Arrange-Act-Assert) pattern.

This module tests the endpoint that retrieves all available activities
and their current participant information.
"""

import pytest


def test_get_all_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all 9 activities with correct structure.
    
    AAA Pattern:
    - Arrange: Set up the test client
    - Act: Call the GET /activities endpoint
    - Assert: Verify all activities are returned with correct structure
    """
    # Arrange
    expected_activities_count = 9
    expected_activity_names = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Tennis Club", "Drama Club", "Art Studio", "Debate Team", "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activities_count
    assert all(name in activities for name in expected_activity_names)


def test_get_all_activities_response_structure(client):
    """
    Test that each activity has the expected data structure.
    
    AAA Pattern:
    - Arrange: Define expected fields for activity objects
    - Act: Call the GET /activities endpoint
    - Assert: Verify each activity has description, schedule, max_participants, and participants
    """
    # Arrange
    expected_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert set(activity_data.keys()) == expected_fields
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_get_all_activities_contains_participants(client):
    """
    Test that activities contain their initial participants.
    
    AAA Pattern:
    - Arrange: Know which activities should have initial participants
    - Act: Call the GET /activities endpoint
    - Assert: Verify participants are present in the response
    """
    # Arrange
    activities_with_participants = {
        "Chess Club": 2,
        "Programming Class": 2,
        "Gym Class": 2,
        "Basketball Team": 1,
        "Tennis Club": 1,
        "Drama Club": 2,
        "Art Studio": 1,
        "Debate Team": 2,
        "Science Club": 1
    }
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, expected_count in activities_with_participants.items():
        assert len(activities[activity_name]["participants"]) == expected_count
