from fastapi import FastAPI
from .api import master_router
from contextlib import asynccontextmanager
from config.logging_config import setup_logging
import logging

setup_logging()

app_logger = logging.getLogger(__name__)


"""
Function Overview:
Lifecycle manager for the FastAPI application, used for setting up resources before the application starts.

Function Logic:
1. Wait for the required resources (if any) to be setup before starting the application.
2. Yield control back to FastAPI to start the app, ensuring setup is completed first.
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Functions to setup any resources will be added here.
    yield


# Create FastAPI app instance and pass lifespan context manager for proper resource management
app = FastAPI(lifespan=lifespan)


# Include the main API router into FastAPI app instance under "Main API Routes" tag for organisation.
app.include_router(master_router, tags=["Main API Routes"])


"""
Endpoint Overview:
Test route to verify if the FastAPI application is running correctly.

Function Logic:
1. The endpoint responds with a simple JSON message indicating that the route was called successfully.

Returns:
- A dictionary with a success message (FastAPI will automatically serialize this to a JSON response).
"""
@app.get('/')
async def read_root():
    app_logger.info("Root endpoint called")
    return {
        "response": "Test route was called successfully.",
        "app_status": "Running."
        }


"""
Endpoint Overview:
Health check route to monitor the FastAPI application.

Function Logic:
1. The endpoint responds with a simple JSON message indicating that the health of the application is OK.

Returns:
- A dictionary with the status of the application.
"""
@app.get('/health')
async def health_check():
    app_logger.info("Health check endpoint called.")
    return {"status": "OK"}
