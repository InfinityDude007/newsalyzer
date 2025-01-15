from fastapi import APIRouter, HTTPException
from app.database import create_user, fetch_user, fetch_id, update_user, delete_user
from app.schema.users import UserDataRequest, UserUpdateRequest, GeneralResponse
from config.logging_config import fastapi_logging
from .utils import LoggingRoute
import logging


# Initialise router and logger
router = APIRouter()
router.route_class = LoggingRoute
fastapi_logging()
logger = logging.getLogger('fastapi_logger')




@router.post("/create", response_model=GeneralResponse)
async def create_new_user(request: UserDataRequest) -> GeneralResponse:
    """
    Endpoint Overview:
    Creates a new user based on the provided data.

    Endpoint Logic:
    1. The endpoint attempts to create a new user by calling the 'create_user' function.
    2. If successful, it returns the response from the 'create_user' function wrapped in the GeneralResponse schema.
    3. If a ValueError is raised, it returns a 409 conflict status with the error message indicating the user creation failed due to invalid data.
    4. If a RuntimeError is raised, it returns a 500 internal server error.

    Parameters:
    request (UserDataRequest): The data for the new user to be created.

    Returns:
    GeneralResponse: A response indicating the outcome of the user creation operation.
    """
    logger.info(f"Create New User endpoint called with request: [{request}]")
    try:
        query_response = await create_user(request)
        return query_response
    
    except ValueError as e:
        logger.error(f"Error creating new user - Value Error: {e}")
        raise HTTPException(status_code=409, detail=str(e))
    
    except RuntimeError as e:
        logger.critical(f"Error creating new user - {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.get("/{id}", response_model=GeneralResponse)
async def fetch_user_data(id: int) -> GeneralResponse:
    """
    Endpoint Overview:
    Fetches data for a specific user based on their ID.

    Endpoint Logic:
    1. The endpoint attempts to fetch user data by calling the 'fetch_user' function with the provided user ID.
    2. If successful, it returns the fetched data wrapped in the GeneralResponse schema.
    3. If a ValueError is raised, it returns a 404 not found status with the error message indicating the requested user does not exist.
    4. If a RuntimeError is raised, it returns a 500 internal server error.

    Parameters:
    id (int): The user ID whose data is to be fetched.

    Returns:
    GeneralResponse: A response containing the user's data or an error message.
    """
    logger.info(f"Fetch User Details endpoint called with ID: {id}")
    try:
        query_response = await fetch_user(id)
        return query_response
    
    except ValueError as e:
        logger.error(f"Error fetching user ID '{id}' - Value Error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except RuntimeError as e:
        logger.critical(f"Error fetching user ID '{id}' - {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.get("/get_id/{username}", response_model=GeneralResponse)
async def fetch_user_id(username: str) -> GeneralResponse:
    """
    Endpoint Overview:
    Fetches the user ID associated with the provided username.

    Endpoint Logic:
    1. The endpoint attempts to fetch the user ID by calling the 'fetch_id' function with the provided username.
    2. If successful, it returns the user ID wrapped in the GeneralResponse schema.
    3. If a ValueError is raised, it returns a 404 not found status with the error message indicating the requested username does not exist.
    4. If a RuntimeError is raised, it returns a 500 internal server error.

    Parameters:
    username (str): The username whose user ID is to be fetched.

    Returns:
    GeneralResponse: A response containing the user ID or an error message.
    """
    logger.info(f"Fetch User ID endpoint called with username: {username}")
    try:
        query_response = await fetch_id(username)
        return query_response
    
    except ValueError as e:
        logger.error(f"Error fetching user ID for '{username}' - Value Error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except RuntimeError as e:
        logger.critical(f"Error fetching user ID for '{username}' - {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.put("/update", response_model=GeneralResponse)
async def update_user_data(request: UserUpdateRequest) -> GeneralResponse:
    """
    Endpoint Overview:
    Updates the data for a specific user based on the provided request.

    Endpoint Logic:
    1. The endpoint attempts to update the user data by calling the 'update_user' function with the provided user data.
    2. If successful, it returns the response from the 'update_user' function wrapped in the GeneralResponse schema.
    3. If a ValueError is raised, a different HTTP status code is returned based on the cause of the error:
        - Returns a 409 conflict status with the error message indicating the user creation failed due to invalid data.
        - Returns a 404 not found status with the error message indicating the requested username does not exist.
    4. If a RuntimeError is raised, it returns a 500 internal server error.

    Parameters:
    request (UserUpdateRequest): The updated data for the user.

    Returns:
    GeneralResponse: A response indicating the outcome of the user data update operation.
    """
    logger.info(f"Update User Details endpoint called with request: [{request}]")
    try:
        query_response = await update_user(request)
        return query_response
    
    except ValueError as e:
        code = 409 if "already exists." in str(e) else 404
        logger.error(f"Error updating data for user ID '{request.user_id}' - Value Error: {e}")
        raise HTTPException(status_code=code, detail=str(e))
    
    except RuntimeError as e:
        logger.critical(f"Error updating data for user ID '{request.user_id}' - {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@router.delete("/delete/{id}", response_model=GeneralResponse)
async def delete_user_data(id: int) -> GeneralResponse:
    """
    Endpoint Overview:
    Deletes the user data for the specified user ID.

    Endpoint Logic:
    1. The endpoint attempts to delete the user data for the provided ID.
    2. If successful, it returns the response from the 'delete_user' function wrapped in the GeneralResponse schema.
    3. If a ValueError is raised, it returns a 404 not found status with the error message indicating the requested user does not exist.
    4. If a RuntimeError is raised, it returns a 500 internal server error.

    Parameters:
    id (int): The user ID whose data is to be deleted.

    Returns:
    GeneralResponse: A response indicating the outcome of the deletion operation.
    """
    logger.info(f"Delete User Details endpoint called with ID: {id}")
    try:
        query_response = await delete_user(id)
        return query_response
    
    except ValueError as e:
        logger.error(f"Error deleting data for user ID '{id}' - Value Error: {e}")
        raise HTTPException(status_code=404, detail=str(e))
    
    except RuntimeError as e:
        logger.critical(f"Error deleting data for user ID '{id}' - {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
