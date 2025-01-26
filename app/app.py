from fastapi import FastAPI
from .api import master_router, LoggingRoute
from contextlib import asynccontextmanager
from config.logging_config import fastapi_logging, healthcheck_logging
import logging


# Initialise loggers
fastapi_logging()
healthcheck_logging()
app_logger = logging.getLogger('fastapi_logger')
health_check_logger = logging.getLogger('health_check_logger')




@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function Overview:
    Lifecycle manager for the FastAPI application, used for setting up resources before the application starts.

    Function Logic:
    1. Wait for the required resources (if any) to be setup before starting the application.
    2. Yield control back to FastAPI to start the app, ensuring setup is completed first.
    """
    # Functions to setup any resources will be added here.
    yield
    # Functions to tear down any resources will be added here.




# Create FastAPI app instance and pass lifespan context manager for proper resource management
app = FastAPI(lifespan=lifespan)

# Include the main API router into FastAPI app instance under "Main API Routes" tag for organisation.
app.include_router(master_router, tags=["Main API Routes"])

# Apply the LoggingRoute middleware to all routes in the app
app.router.route_class = LoggingRoute




@app.get('/')
async def read_root() -> dict:
    """
    Endpoint Overview:
    Main entry point of the FastAPI web application.

    Function Logic:
    1. The endpoint responds with a simple 'welcome' JSON message.

    Returns:
    - A dictionary with a welcome message.
    """
    app_logger.info("Tag: General - Endpoint: Root - Request: None")
    return {
        "response": "Welcome to Newsalyzer!",
        }




@app.get('/health')
async def health_check() -> dict:
    """
    Endpoint Overview:
    Health check route to monitor the FastAPI application.

    Function Logic:
    1. The endpoint responds with a simple JSON message indicating that the health of the application is OK.

    Returns:
    - A dictionary with the status of the application.
    """
    health_check_logger.info("FastAPI application healthy.")
    return {"status": "healthy"}
