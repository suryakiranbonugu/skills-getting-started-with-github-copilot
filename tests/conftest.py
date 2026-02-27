"""
Pytest configuration and shared fixtures for the test suite.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Store the original activities state for reset between tests
INITIAL_ACTIVITIES_STATE = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for intramural and inter-school games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and participate in friendly matches",
        "schedule": "Saturdays, 10:00 AM - 11:30 AM",
        "max_participants": 10,
        "participants": ["noah@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions and improve acting skills",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 25,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and critical thinking skills through competitive debate",
        "schedule": "Mondays and Fridays, 3:30 PM - 4:45 PM",
        "max_participants": 16,
        "participants": ["liam@mergington.edu", "lucas@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts through hands-on activities",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["mason@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities_state():
    """
    Fixture that resets the activities dictionary to its initial state before each test.
    This ensures test isolation and prevents tests from affecting each other.
    
    autouse=True means this fixture runs automatically before each test function.
    """
    # Reset the global activities dictionary
    activities.clear()
    activities.update({k: {kk: v.copy() if isinstance(v, list) else v 
                           for kk, v in vv.items()} 
                      for k, vv in INITIAL_ACTIVITIES_STATE.items()})
    
    yield


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance for the FastAPI app.
    This client can be used to make requests to the application endpoints.
    """
    return TestClient(app)
