from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime


class UserDataRequest(BaseModel):
    """
    Class Overview:
    Schema for requests containing all data necessary for creating a new user.

    Attributes:
    email_id (str): The email address of the user.
    username (str): The username of the user.
    password (str): The password for the user.
    first_name (str): The first name of the user.
    last_name (Optional[str]): The last name of the user (if provided).
    """
    email_id: str
    username: str
    password: str
    first_name: str
    last_name: Optional[str] = None


class UserDataResponse(BaseModel):
    """
    Class Overview:
    Schema for responses containing all data related to a user.

    Attributes:
    user_id (int): The unique identifier of the user.
    email_id (str): The email address of the user.
    username (str): The username of the user.
    password (str): The password for the user.
    first_name (str): The first name of the user.
    last_name (Optional[str]): The last name of the user (if provided).
    created_at (datetime): The timestamp indicating when the user account was created.
    """
    user_id: int
    email_id: str
    username: str
    password: str
    first_name: str
    last_name: Optional[str] = None
    created_at: datetime


class UserUpdateRequest(BaseModel):
    """
    Class Overview:
    Schema for requests containing data to update a user's information.

    Attributes:
    user_id (int): The unique identifier of the user whose data is to be updated.
    field (str): The field in the user's data that is to be updated ('email', 'username', 'first_name' or 'last_name').
    data (str): The new value to be set for the specified field.
    """
    user_id: int
    field: str
    data: str


class GeneralResponse(BaseModel):
    """
    Class Overview:
    Schema for responding with details about the outcome of any operation.

    Attributes:
    detail (str): A message describing the outcome of the operation.
    data (Union[None, str, int, UserDataResponse]): The data related to the operation, which can be empty (none), an ID, a username, or user data wrapped in the UserDataResponse schema.
    """
    detail: str
    data: Union[None, str, int, UserDataResponse]
