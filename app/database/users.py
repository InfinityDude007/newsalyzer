import os
from dotenv import load_dotenv
from supabase import create_client
from postgrest.exceptions import APIError


load_dotenv()
DATABASE_URL = os.getenv('SUPABASE_URL')
DATABASE_API_KEY = os.getenv('SUPABASE_API_KEY')
database_client = create_client(DATABASE_URL, DATABASE_API_KEY)


# Create new user:
def create_user(data: dict):
    try:
        response = database_client.table("users").insert(data).execute()
        if response.data:
            username = data["username"]
            print(f"User '{username}' created successfully.")
        else:
            raise Exception("Unknown error occurred while trying to create a new user.")
    except APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


# Fetch all user data:
def fetch_user(id: int):
    try:
        response = database_client.table("users").select("*").eq("user_id", id).execute()
        if response.data:
            print(response.data[0])
        elif not response.data:
            raise Exception(f"User ID '{id}' not found.")
        else:
            raise Exception("Unknown error occurred while trying to fetch user details.")
    except APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


# Fetch user ID by username:
def fetch_user_id(username: str):
    try:
        response = database_client.table("users").select("user_id").eq("username", username).execute()
        if response.data:
            print(response.data[0]["user_id"])
        elif not response.data:
            raise Exception(f"User with username '{username}' not found.")
        else:
            raise Exception("Unknown error occurred while trying to fetch user ID.")
    except APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


# Update user data:
def update_user(id: int, field: str, data: str):
    try:
        response = database_client.table("users").update({field: data}).eq("user_id", id).execute()
        if response.data:
            if field == "first_name" or field == "last_name" or field == "email_id":
                field = field.replace('_', ' ')
            print(f"{field.capitalize()} updated successfully for user ID: {id}.")
        elif not response.data:
            raise Exception(f"User ID '{id}' not found.")
        else:
            raise Exception("Unknown error occurred while trying to update user details.")
    except APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


# Delete user data:
def delete_user(id: int):
    try:
        response = database_client.table("users").delete().eq("user_id", id).execute()
        if response.data:
            print(f"User details deleted successfully for user ID: {id}.")
        elif not response.data:
            raise Exception(f"User ID '{id}' not found.")
        else:
            raise Exception("Unknown error occurred while trying to delete user details.")
    except APIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
