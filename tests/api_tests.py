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




"""
General App Endpoints
"""


# Root (http://localhost:port/)
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_root_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/")

    expected_body = {"response": "Welcome to Newsalyzer!"}
    expected_status = 200
    pass_flag = True
    
    if response.json() != expected_body:
        tests_logger.error("Tag: General - Endpoint: Root - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response.json(), expected_body)
        pass_flag = False
    if response.status_code != expected_status:
        tests_logger.error("Tag: General - Endpoint: Root - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response), expected_status)
        pass_flag = False
    if pass_flag:
        tests_logger.info(f"Tag: General - Endpoint: Root - Test Status - PASSED - HTTP Response: {get_http_status(response)}")

    assert response.json() == expected_body, f"Unexpected response body for Root endpoint: {response.json()} (expected: {expected_body})"
    assert response.status_code == expected_status, f"Unexpected status code for Root endpoint: {get_http_status(response)} (expected: {expected_status} OK)"


# Health Check (http://localhost:port/health)
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_health_endpoint():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/health")
    
    expected_body = {"status": "healthy"}
    expected_status = 200
    pass_flag = True
    
    if response.json() != expected_body:
        tests_logger.error("Tag: General - Endpoint: Health Check - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)\n", response.json(), expected_body)
        pass_flag = False
    if response.status_code != expected_status:
        tests_logger.error("Tag: General - Endpoint: Health Check - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)\n", get_http_status(response), expected_status)
        pass_flag = False
    if pass_flag:
        tests_logger.info(f"Tag: General - Endpoint: Health Check - Test Status - PASSED - HTTP Response: {get_http_status(response)}\n")
    
    assert response.json() == expected_body, f"Unexpected response body for Health Check endpoint: {response.json()} (expected: {expected_body})"
    assert response.status_code == expected_status, f"Unexpected status code for Health Check endpoint: {get_http_status(response)} (expected: {expected_status} OK)"




"""
Users Table Endpoints
"""


# Create New User (http://localhost:port/users/create)
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_create_user_endpoint():
    async with httpx.AsyncClient() as client:
        request1 = {
            "email_id": "test.user1@gmail.com",
            "username": "TestUser_101",
            "password": "TestPswrd123!",
            "first_name": "Test",
            "last_name": "User 1"
        }
        request2 = {
            "email_id": "testing.user1@gmail.com",
            "username": "TestUser_101",
            "password": "TestPswrd123!",
            "first_name": "Test",
            "last_name": "User 1"
        }
        response1 = await client.post(f"{base_url}/users/create", json=request1)
        response2 = await client.post(f"{base_url}/users/create", json=request1)
        response3 = await client.post(f"{base_url}/users/create", json=request2)

    request_email_id = request1["email_id"]
    request_username = request2["username"]
    expected_body1 = f"User '{request_username}' created successfully."
    expected_body2 = f"User with email ID '{request_email_id}' already exists."
    expected_body3 = f"User with username '{request_username}' already exists."
    expected_status1 = 200
    expected_status2 = expected_status3 = 409
    pass_flag = True

    if (response1.json())["detail"] != expected_body1:
        tests_logger.error("Tag: Users - Endpoint: Create New User - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response1.json(), expected_body1)
        pass_flag = False
    if response1.status_code != expected_status1:
        tests_logger.error("Tag: Users - Endpoint: Create New User - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response1), expected_status1)
        pass_flag = False
    assert (response1.json())["detail"] == expected_body1, f"Unexpected response body for Create New User endpoint: {response1.json()} (expected: {expected_body1})"
    assert response1.status_code == expected_status1, f"Unexpected status code for Create New User endpoint: {get_http_status(response1)} (expected: {expected_status1} OK)"

    if (response2.json())["detail"] != expected_body2:
        tests_logger.error("Tag: Users - Endpoint: Create New User - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response2.json(), expected_body2)
        pass_flag = False
    if response2.status_code != expected_status2:
        tests_logger.error("Tag: Users - Endpoint: Create New User - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response2), expected_status2)
        pass_flag = False
    assert (response2.json())["detail"] == expected_body2, f"Unexpected response body for Create New User endpoint: {response2.json()} (expected: {expected_body2})"
    assert response2.status_code == expected_status2, f"Unexpected status code for Create New User endpoint: {get_http_status(response2)} (expected: {expected_status2} OK)"
    
    if (response3.json())["detail"] != expected_body3:
        tests_logger.error("Tag: Users - Endpoint: Create New User - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response3.json(), expected_body3)
        pass_flag = False
    if response3.status_code != expected_status3:
        tests_logger.error("Tag: Users - Endpoint: Create New User - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response3), expected_status3)
        pass_flag = False
    assert (response3.json())["detail"] == expected_body3, f"Unexpected response body for Create New User endpoint: {response3.json()} (expected: {expected_body3})"
    assert response3.status_code == expected_status3, f"Unexpected status code for Create New User endpoint: {get_http_status(response3)} (expected: {expected_status3} OK)"
    
    if pass_flag:
        tests_logger.info(f"Tag: Users - Endpoint: Create New User - Test Status - PASSED - HTTP Response: {get_http_status(response1)}")


# Fetch User ID by Username (http://localhost:port/users/get_id/{username})
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_fetch_user_id_endpoint():
    async with httpx.AsyncClient() as client:
        username1 = "TestUser_101"
        username2= "NonExistentUser"
        response1 = await client.get(f"{base_url}/users/get_id/{username1}")
        response2 = await client.get(f"{base_url}/users/get_id/{username2}")

    expected_body1 = f"User ID for username '{username1}' fetched successfully."
    expected_body2 = f"Username '{username2}' not found."
    expected_status1 = 200
    expected_status2 = 404
    pass_flag = True

    response1_detail = (response1.json())["detail"]
    if  response1_detail != expected_body1:
        tests_logger.error("Tag: Users - Endpoint: Fetch User ID - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response1_detail, expected_body1)
        pass_flag = False
    if response1.status_code != expected_status1:
        tests_logger.error("Tag: Users - Endpoint: Fetch User ID - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response1), expected_status1)
        pass_flag = False
    assert response1_detail == expected_body1, f"Unexpected response body for Fetch User ID endpoint: {response1_detail} (expected: {expected_body1})"
    assert response1.status_code == expected_status1, f"Unexpected status code for Fetch User ID endpoint: {get_http_status(response1)} (expected: {expected_status1} OK)"

    response2_detail = (response2.json())["detail"]
    if response2_detail != expected_body2:
        tests_logger.error("Tag: Users - Endpoint: Fetch User ID - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response2_detail, expected_body2)
        pass_flag = False
    if response2.status_code != expected_status2:
        tests_logger.error("Tag: Users - Endpoint: Fetch User ID - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response2), expected_status2)
        pass_flag = False
    assert response2_detail == expected_body2, f"Unexpected response body for Fetch User ID endpoint: {response2_detail} (expected: {expected_body2})"
    assert response2.status_code == expected_status2, f"Unexpected status code for Fetch User ID endpoint: {get_http_status(response2)} (expected: {expected_status2} OK)"
    
    if pass_flag:
        tests_logger.info(f"Tag: Users - Endpoint: Fetch User ID - Test Status - PASSED - HTTP Response: {get_http_status(response1)}")


# Fetch User Details (http://localhost:port/users/{id})
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_fetch_user_details_endpoint():
    async with httpx.AsyncClient() as client:
        get_id = await client.get(f"{base_url}/users/get_id/TestUser_101")
        id1 = (get_id.json())["data"]
        id2= 1
        response1 = await client.get(f"{base_url}/users/{id1}")
        response2 = await client.get(f"{base_url}/users/{id2}")

    expected_body1 = f"Details for user ID '{id1}' fetched successfully."
    expected_body2 = f"User ID '{id2}' not found."
    expected_status1 = 200
    expected_status2 = 404
    pass_flag = True

    response1_detail = (response1.json())["detail"]
    if  response1_detail != expected_body1:
        tests_logger.error("Tag: Users - Endpoint: Fetch User Details - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response1_detail, expected_body1)
        pass_flag = False
    if response1.status_code != expected_status1:
        tests_logger.error("Tag: Users - Endpoint: Fetch User Details - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response1), expected_status1)
        pass_flag = False
    assert response1_detail == expected_body1, f"Unexpected response body for Fetch User Details endpoint: {response1_detail} (expected: {expected_body1})"
    assert response1.status_code == expected_status1, f"Unexpected status code for Fetch User Details endpoint: {get_http_status(response1)} (expected: {expected_status1} OK)"

    response2_detail = (response2.json())["detail"]
    if response2_detail != expected_body2:
        tests_logger.error("Tag: Users - Endpoint: Fetch User Details - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response2_detail, expected_body2)
        pass_flag = False
    if response2.status_code != expected_status2:
        tests_logger.error("Tag: Users - Endpoint: Fetch User Details - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response2), expected_status2)
        pass_flag = False
    assert response2_detail == expected_body2, f"Unexpected response body for Fetch User Details endpoint: {response2_detail} (expected: {expected_body2})"
    assert response2.status_code == expected_status2, f"Unexpected status code for Fetch User Details endpoint: {get_http_status(response2)} (expected: {expected_status2} OK)"
    
    if pass_flag:
        tests_logger.info(f"Tag: Users - Endpoint: Fetch User Details - Test Status - PASSED - HTTP Response: {get_http_status(response1)}")


# Update User Details (http://localhost:port/users/update)
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_update_user_details_endpoint():
    async with httpx.AsyncClient() as client:
        request1 = {
            "email_id": "test.user2@gmail.com",
            "username": "TestUser_102",
            "password": "TestPswrd123!",
            "first_name": "Test",
            "last_name": "User 2"
        }
        create_temp_user = await client.post(f"{base_url}/users/create", json=request1)
        get_id = await client.get(f"{base_url}/users/get_id/TestUser_102")
        id1 = (get_id.json())["data"]
        id2 = 1
        request2 = {"user_id": id1, "field": "email_id", "data": "tested_user2@gmail.com"}
        request3 = {"user_id": id1, "field": "username", "data": "TestUser_202"}
        request4 = {"user_id": id1, "field": "password", "data": "TestNewPswrd123!"}
        request5 = {"user_id": id1, "field": "first_name", "data": "User 2"}
        request6 = {"user_id": id1, "field": "last_name", "data": "Test"}
        request7 = {"user_id": id1, "field": "email_id", "data": "test.user1@gmail.com"}
        request8 = {"user_id": id1, "field": "username", "data": "TestUser_101"}
        request9 = {"user_id": id2, "field": "username", "data": "TestUser_101"}
        response2 = await client.put(f"{base_url}/users/update", json=request2)
        response3 = await client.put(f"{base_url}/users/update", json=request3)
        response4 = await client.put(f"{base_url}/users/update", json=request4)
        response5 = await client.put(f"{base_url}/users/update", json=request5)
        response6 = await client.put(f"{base_url}/users/update", json=request6)
        response7 = await client.put(f"{base_url}/users/update", json=request7)
        response8 = await client.put(f"{base_url}/users/update", json=request8)
        response9 = await client.put(f"{base_url}/users/update", json=request9)

    # Helper function to format expected body based on request.
    def format_body(response, user_id):
        field = response["field"]
        if field == "first_name" or field == "last_name" or field == "email_id":
            field = field.replace('_', ' ')
        return f"{field.capitalize()} updated successfully for user ID '{user_id}'."

    request7_data = request7["data"]
    request8_data = request8["data"]
    expected_body2 = format_body(request2, id1)
    expected_body3 = format_body(request3, id1)
    expected_body4 = format_body(request4, id1)
    expected_body5 = format_body(request5, id1)
    expected_body6 = format_body(request6, id1)
    expected_body7 = f"User with email ID '{request7_data}' already exists."
    expected_body8 = f"User with username '{request8_data}' already exists."
    expected_body9 = f"User ID '{id2}' not found."
    expected_status2 = 200
    expected_status3 = 409
    expected_status4 = 404
    pass_flag = True

    response_arr = [response2, response3, response4, response5, response6, response7, response8, response9]
    body_arr = [expected_body2, expected_body3, expected_body4, expected_body5, expected_body6, expected_body7, expected_body8, expected_body9]
    status_arr = [expected_status2, expected_status2, expected_status2, expected_status2, expected_status2, expected_status3, expected_status3, expected_status4]
    for i in range(len(response_arr) - 1):
        response = response_arr[i]
        body = body_arr[i]
        status = status_arr[i]
        response_detail = (response.json())["detail"]
        if  response_detail != body:
            tests_logger.error("Tag: Users - Endpoint: Update User Details - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response_detail, body)
            pass_flag = False
        if response.status_code != status:
            tests_logger.error("Tag: Users - Endpoint: Update User Details - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response), status)
            pass_flag = False
        assert response_detail == body, f"Unexpected response body for Update User Details endpoint: {response_detail} (expected: {body})"
        assert response.status_code == status, f"Unexpected status code for Update User Details endpoint: {get_http_status(response)} (expected: {status} OK)"
    
    if pass_flag:
        tests_logger.info(f"Tag: Users - Endpoint: Update User Details - Test Status - PASSED - HTTP Response: {get_http_status(response6)}")


# Delete User (http://localhost:port/users/delete/{id})
@pytest.mark.asyncio
@pytest.mark.fastapi
async def test_delete_user_endpoint():
    async with httpx.AsyncClient() as client:
        get_id1 = await client.get(f"{base_url}/users/get_id/TestUser_101")
        get_id2 = await client.get(f"{base_url}/users/get_id/TestUser_202")
        id1 = (get_id1.json())["data"]
        id2 = (get_id2.json())["data"]
        id3 = 1
        response1 = await client.delete(f"{base_url}/users/delete/{id1}")
        response2 = await client.delete(f"{base_url}/users/delete/{id2}")
        response3 = await client.delete(f"{base_url}/users/delete/{id3}") 

    expected_body1 = f"User details deleted successfully for user ID '{id1}'."
    expected_body2 = f"User details deleted successfully for user ID '{id2}'."
    expected_body3 = f"User ID '{id3}' not found."
    expected_status1 = 200
    expected_status2 = 404
    pass_flag = True

    response1_detail = (response1.json())["detail"]
    if  response1_detail != expected_body1:
        tests_logger.error("Tag: Users - Endpoint: Delete User - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response1_detail, expected_body1)
        pass_flag = False
    if response1.status_code != expected_status1:
        tests_logger.error("Tag: Users - Endpoint: Delete User - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response1), expected_status1)
        pass_flag = False
    assert response1_detail == expected_body1, f"Unexpected response body for Delete User endpoint: {response1_detail} (expected: {expected_body1})"
    assert response1.status_code == expected_status1, f"Unexpected status code for Delete User endpoint: {get_http_status(response1)} (expected: {expected_status1} OK)"

    response2_detail = (response2.json())["detail"]
    if response2_detail != expected_body2:
        tests_logger.error("Tag: Users - Endpoint: Delete User - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response2_detail, expected_body2)
        pass_flag = False
    if response2.status_code != expected_status1:
        tests_logger.error("Tag: Users - Endpoint: Delete User - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response2), expected_status1)
        pass_flag = False
    assert response2_detail == expected_body2, f"Unexpected response body for Delete User endpoint: {response2_detail} (expected: {expected_body2})"
    assert response2.status_code == expected_status1, f"Unexpected status code for Delete User endpoint: {get_http_status(response2)} (expected: {expected_status1} OK)"

    response3_detail = (response3.json())["detail"]
    if response3_detail != expected_body3:
        tests_logger.error("Tag: Users - Endpoint: Delete User - Test Status: FAILED - Cause: Unexpected response body: %s (expected: %s)", response3_detail, expected_body3)
        pass_flag = False
    if response3.status_code != expected_status2:
        tests_logger.error("Tag: Users - Endpoint: Delete User - Test Status: FAILED - Cause: Unexpected status code: %s (expected: %s OK)", get_http_status(response3), expected_status2)
        pass_flag = False
    assert response3_detail == expected_body3, f"Unexpected response body for Delete User endpoint: {response3_detail} (expected: {expected_body3})"
    assert response3.status_code == expected_status2, f"Unexpected status code for Delete User endpoint: {get_http_status(response3)} (expected: {expected_status2} OK)"
    
    if pass_flag:
        tests_logger.info(f"Tag: Users - Endpoint: Delete User - Test Status - PASSED - HTTP Response: {get_http_status(response2)}\n")
