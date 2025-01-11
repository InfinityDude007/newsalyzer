import requests
import pytest
import os
from dotenv import load_dotenv


"""
Test file to setup tests for all created FastAPI endpoints to validate status code and responses of all app endpoints.
Ensure endpoints behave as expected and proper handling of edge cases, errors and failures.
"""


load_dotenv()
SERVER_PORT = os.getenv('SERVER_PORT', 9000)
base_url = f"http://localhost:{SERVER_PORT}"


# Helper function to return the HTTP status code and reason phrase (e.g., '200 OK').
def get_http_status(response):
    return f"{response.status_code} {response.reason}"


# Root endpoint (http://localhost:port/)
@pytest.mark.fastapi
def test_root_endpoint():
    response = requests.get(f"{base_url}/")
    expected_body = {"response": "Welcome to Newsalyzer!"}
    expected_status = 200
    assert response.json() == expected_body, f"Unexpected response body for Root endpoint: {response.json()} (expected: {expected_body})"
    assert response.status_code == expected_status, f"Unexpected status code for Root endpoint: {get_http_status(response)} (expected: {expected_status} OK)"


# Health check endpoint (http://localhost:port/health)
@pytest.mark.fastapi
def test_health_endpoint():
    response = requests.get(f"{base_url}/health")
    expected_body = {"status": "healthy"}
    expected_status = 200
    assert response.json() == expected_body, f"Unexpected response body for Health Check endpoint: {response.json()} (expected: {expected_body})"
    assert response.status_code == expected_status, f"Unexpected status code for Health Check endpoint: {get_http_status(response)} (expected: {expected_status} OK)"
