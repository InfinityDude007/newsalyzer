"""
Test file to setup tests for all created FastAPI endpoints to validate status code and responses of all app endpoints.
Ensure endpoints behave as expected and proper handling of edge cases, errors and failures.
"""


import httpx
from config.logging_config import setup_tests_logging
import logging
import pytest
import os
from dotenv import load_dotenv


setup_tests_logging()
tests_logger = logging.getLogger('tests_logger')


load_dotenv()
SERVER_PORT = os.getenv('SERVER_PORT', 9000)
base_url = f"http://localhost:{SERVER_PORT}"


# Helper function to return the HTTP status code and reason phrase (e.g., '200 OK').
def get_http_status(response):
    return f"{response.status_code} {response.reason_phrase}"


# Root endpoint (http://localhost:port/)
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_root_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/")

    expected_body = {"response": "Welcome to Newsalyzer!"}
    expected_status = 200
    pass_flag = True
    
    if response.json() != expected_body:
        tests_logger.error("Unexpected response body for Root endpoint: %s (expected: %s)", response.json(), expected_body)
        pass_flag = False
    if response.status_code != expected_status:
        tests_logger.error("Unexpected status code for Root endpoint: %s (expected: %s OK)", get_http_status(response), expected_status)
        pass_flag = False
    if pass_flag:
        tests_logger.info(f"Test passed - Root endpoint - {get_http_status(response)}")

    assert response.json() == expected_body, f"Unexpected response body for Root endpoint: {response.json()} (expected: {expected_body})"
    assert response.status_code == expected_status, f"Unexpected status code for Root endpoint: {get_http_status(response)} (expected: {expected_status} OK)"


# Health check endpoint (http://localhost:port/health)
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_health_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/health")
    
    expected_body = {"status": "healthy"}
    expected_status = 200
    pass_flag = True
    
    if response.json() != expected_body:
        tests_logger.error("Unexpected response body for Health Check endpoint: %s (expected: %s)", response.json(), expected_body)
        pass_flag = False
    if response.status_code != expected_status:
        tests_logger.error("Unexpected status code for Health Check endpoint: %s (expected: %s OK)", get_http_status(response), expected_status)
        pass_flag = False
    if pass_flag:
        tests_logger.info(f"Test passed - Health Check endpoint - Status: {get_http_status(response)}")
    
    assert response.json() == expected_body, f"Unexpected response body for Health Check endpoint: {response.json()} (expected: {expected_body})"
    assert response.status_code == expected_status, f"Unexpected status code for Health Check endpoint: {get_http_status(response)} (expected: {expected_status} OK)"
