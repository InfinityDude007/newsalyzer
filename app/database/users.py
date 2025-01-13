import os
from dotenv import load_dotenv
from supabase import create_client
from postgrest.exceptions import APIError
from app.schema.users import UserDataRequest, UserDataResponse, UserUpdateRequest, GeneralResponse


load_dotenv()
DATABASE_URL = os.getenv('SUPABASE_URL')
DATABASE_API_KEY = os.getenv('SUPABASE_API_KEY')
database_client = create_client(DATABASE_URL, DATABASE_API_KEY)




async def create_user(data: UserDataRequest) -> GeneralResponse:
    """
    Function Overview:
    Creates a new user based on the provided data.

    Function Logic:
    1. The function attempts to create a new user with the given request data.
    2. If successful, it returns a structured response wrapped in the GeneralResponse schema.
    3. Depending on the error raised:
        - ValueError: Returns a structured response indicating the given email ID or username is in use by another user.
        - APIError, Exception or an Unexpected Error:  Raises a RuntimeError with a detailed error message.

    Parameters:
    request (UserDataRequest): Data required to create a new user.

    Returns:
    GeneralResponse: A response containing the result of the user creation operation.
    """
    try:
        request_dict = data.model_dump()
        response = (
            database_client
            .table("users")
            .insert(request_dict)
            .execute()
            )

        if response.data:
            return GeneralResponse(
                detail = f"User '{data.username}' created successfully.",
                data = None
                )
        else:
            raise Exception("Unknown error occurred while trying to create a new user.")
        
    except APIError as e:

        if (e.json()["code"] == "23505"):
            error_detail = (
                e.json()["details"]
                ).split(" ")
            error_field = error_detail[1]

            if "email_id" in error_field:
                raise ValueError(f"User with email ID '{data.email_id}' already exists.")
            
            if "username" in error_field:
                raise ValueError(f"User with username '{data.username}' already exists.")
            
            else:
                raise RuntimeError(f"API Error: {e}") from e
            
        else:
            raise RuntimeError(f"API Error: {e}") from e

    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {e}") from e




async def fetch_user(id: int) -> GeneralResponse:
    """
    Function Overview:
    Fetches the data of a user based on the given user ID.

    Function Logic:
    1. The function attempts to fetch user data for the provided user ID.
    2. If successful, it returns a structured response wrapped in the GeneralResponse schema.
    3. Depending on the error raised:
        - ValueError: Returns a structured response indicating the requested user does not exist.
        - APIError, Exception or an Unexpected Error:  Raises a RuntimeError with a detailed error message.

    Parameters:
    id (int): The user ID whose data is to be fetched.

    Returns:
    GeneralResponse: A response containing the result of the fetch operation and the requested user's data.
    """
    try:
        response = (
            database_client
            .table("users")
            .select("*")
            .eq("user_id", id)
            .execute()
            )
        
        if response.data:
            return GeneralResponse(
                detail = f"Details for user ID '{id}' fetched successfully.", 
                data = UserDataResponse(**(response.data[0]))
                )
        elif not response.data:
            raise ValueError()
        else:
            raise Exception("Unknown error occurred while trying to fetch user details.")
        
    except APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    
    except ValueError as e:
        raise ValueError(f"User ID '{id}' not found.") from e
    
    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {e}") from e




async def fetch_id(username: str) -> GeneralResponse:
    """
    Function Overview:
    Fetches the user ID based on the provided username.

    Function Logic:
    1. The function attempts to fetch the user ID for the given username.
    2. If successful, it returns a structured response wrapped in the GeneralResponse schema.
    3. Depending on the error raised:
        - ValueError: Returns a structured response indicating the requested user does not exist.
        - APIError, Exception or an Unexpected Error:  Raises a RuntimeError with a detailed error message.

    Parameters:
    username (str): The username for which the user ID is to be fetched.

    Returns:
    GeneralResponse: A response containing the result of the fetch operation and the user ID associated with the requested username.
    """
    try:
        response = (
            database_client
            .table("users")
            .select("user_id")
            .eq("username", username)
            .execute()
            )

        if response.data:
            return GeneralResponse(
                detail = f"User ID for username '{username}' fetched successfully.", 
                data = response.data[0]["user_id"]
                )
        elif not response.data:
            raise ValueError()
        else:
            raise Exception("Unknown error occurred while trying to fetch user ID.")
        
    except APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    
    except ValueError as e:
        raise ValueError(f"Username '{username}' not found.") from e

    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {e}") from e




async def update_user(request: UserUpdateRequest) -> GeneralResponse:
    """
    Function Overview:
    Updates the data for an existing user.

    Function Logic:
    1. The function attempts to update user data based on the provided request.
    2. If successful, it returns a structured response wrapped in the GeneralResponse schema.
    3. Depending on the error raised:
        - ValueError: Returns a structured response indicating the given email ID or username is in use by another user
        - APIError, Exception or an Unexpected Error:  Raises a RuntimeError with a detailed error message.

    Parameters:
    request (UserUpdateRequest): Data to update the existing user.

    Returns:
    GeneralResponse: A response indicating the outcome of the update operation.
    """
    try:
        id = request.user_id
        field = request.field
        data = request.data
        response = (
            database_client
            .table("users")
            .update({field: data})
            .eq("user_id", id)
            .execute()
            )
        
        if response.data:
            if field == "first_name" or field == "last_name" or field == "email_id":
                field = field.replace('_', ' ')
            return GeneralResponse(
                detail = f"{field.capitalize()} updated successfully for user ID '{id}'.",
                data = None
                )
        elif not response.data:
            raise ValueError()
        else:
            raise Exception("Unknown error occurred while trying to update user details.")
        
    except APIError as e:
        if (e.json()["code"] == "23505"):
            error_detail = (
                e.json()["details"]
                ).split(" ")
            error_field = error_detail[1]

            if "email_id" in error_field:
                raise ValueError(f"User with email ID '{request.data}' already exists.")
            
            if "username" in error_field:
                raise ValueError(f"User with username '{request.data}' already exists.")
            
            else:
                raise RuntimeError(f"API Error: {e}") from e
            
        else:
            raise RuntimeError(f"API Error: {e}") from e
    
    except ValueError as e:
        raise ValueError(f"User ID '{id}' not found.") from e

    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {e}") from e




async def delete_user(id: int) -> GeneralResponse:
    """
    Function Overview:
    Deletes the user data for the specified user ID.

    Function Logic:
    1. The function attempts to delete the user data for the provided ID.
    2. If successful, it returns a structured response wrapped in the GeneralResponse schema.
    3. Depending on the error raised:
        - ValueError: Returns a structured response indicating the requested user does not exist.
        - APIError, Exception or an Unexpected Error:  Raises a RuntimeError with a detailed error message.

    Parameters:
    id (int): The user ID whose data is to be deleted.

    Returns:
    GeneralResponse: A response indicating the outcome of the deletion operation.
    """
    try:
        response = (
            database_client
            .table("users")
            .delete()
            .eq("user_id", id)
            .execute()
            )
        
        if response.data:
            return GeneralResponse(
                detail = f"User details deleted successfully for user ID '{id}'.",
                data = None
                )
        elif not response.data:
            raise ValueError()
        else:
            raise Exception("Unknown error occurred while trying to delete user details.")
        
    except APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    
    except ValueError as e:
        raise ValueError(f"User ID '{id}' not found.") from e

    except Exception as e:
        raise RuntimeError(f"Unexpected Error: {e}")
