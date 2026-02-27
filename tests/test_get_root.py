"""
Tests for GET / endpoint using AAA (Arrange-Act-Assert) pattern.

This module tests the root endpoint which redirects to the static frontend.
"""

import pytest


def test_root_redirects_to_static_index(client):
    """
    Test that GET / redirects to the static index.html file.
    
    AAA Pattern:
    - Arrange: Set up the test client
    - Act: Call the GET / endpoint
    - Assert: Verify redirect status code and location header
    """
    # Arrange
    # (TestClient is configured to follow redirects by default, so we need follow_redirects=False)
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code in [307, 308]  # Temporary or permanent redirect
    assert "location" in response.headers
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_target_is_correct(client):
    """
    Test that the redirect URL points to the correct static file.
    
    AAA Pattern:
    - Arrange: Set up the test client
    - Act: Call the GET / endpoint without following redirects
    - Assert: Verify the location header contains the expected path
    """
    # Arrange
    expected_redirect_path = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.headers.get("location") == expected_redirect_path


def test_root_response_is_redirect_status(client):
    """
    Test that the root endpoint returns a redirect status code.
    
    AAA Pattern:
    - Arrange: Know that redirect responses are 3xx status codes
    - Act: Call the GET / endpoint without following redirects
    - Assert: Verify response status code is in the 3xx range
    """
    # Arrange
    # Status codes 307 and 308 are temporary/permanent redirects
    valid_redirect_codes = {307, 308}
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code in valid_redirect_codes
