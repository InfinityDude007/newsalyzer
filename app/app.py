from fastapi import FastAPI, Request, Response
from fastapi.routing import APIRoute
from http import HTTPStatus
from .api import master_router
from contextlib import asynccontextmanager
from config.logging_config import fastapi_logging, healthcheck_logging
import logging


# Initialise loggers
fastapi_logging()
healthcheck_logging()
app_logger = logging.getLogger('fastapi_logger')
health_check_logger = logging.getLogger('health_check_logger')


"""
Class Overview:
Custom middleware class to log HTTP response details for each request processed by the FastAPI application.

Function Logic:
1. Overrides the `get_route_handler` method from `APIRoute`.
2. Wraps the original route handler with a custom handler that intercepts the response.
3. Logs the HTTP response details:
   - If the request URL contains "/health", it uses the health check logger.
   - Otherwise, it uses the default app logger.
4. Retrieves the status phrase for the response status code, defaulting to "Unknown" if the code is not standard.

Returns:
- The original response object after logging details.
"""
class LoggingRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request):
            response: Response = await original_route_handler(request)
            logger = app_logger if "/health" not in str(request.url) else health_check_logger
            status_phrase = HTTPStatus(response.status_code).phrase if response.status_code in HTTPStatus._value2member_map_ else "Unknown"
            logger.debug(f"HTTP Response: {response.status_code} {status_phrase}")
            return response
        return custom_route_handler


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
    # Functions to tear down any resources will be added here.


# Create FastAPI app instance and pass lifespan context manager for proper resource management
app = FastAPI(lifespan=lifespan)


# Include the main API router into FastAPI app instance under "Main API Routes" tag for organisation.
app.include_router(master_router, tags=["Main API Routes"])


# Apply the LoggingRoute middleware to all routes in the app
app.router.route_class = LoggingRoute


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
    app_logger.info("Root endpoint called.")
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
    health_check_logger.info("FastAPI health check called.")
    return {"status": "OK"}
