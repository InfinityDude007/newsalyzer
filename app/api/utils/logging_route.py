from fastapi import Request, Response, HTTPException
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from http import HTTPStatus
from config.logging_config import fastapi_logging, healthcheck_logging
import logging


# Initialise loggers
fastapi_logging()
healthcheck_logging()
app_logger = logging.getLogger('fastapi_logger')
health_check_logger = logging.getLogger('health_check_logger')


class LoggingRoute(APIRoute):
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
    def get_route_handler(self):

        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request):

            logger = app_logger if "/health" not in str(request.url) else health_check_logger
            try:
                response: Response = await original_route_handler(request)
                try:
                    status_phrase = HTTPStatus(response.status_code).phrase
                except ValueError:
                    status_phrase = "Unknown"
                logger.debug(f"HTTP Response: {response.status_code} {status_phrase}\n")
                return response

            except HTTPException as e:
                try:
                    status_phrase = HTTPStatus(e.status_code).phrase
                except ValueError:
                    status_phrase = "Unknown"
                logger.debug(f"HTTP Response: {e.status_code} {status_phrase}\n")
                return JSONResponse(
                    content = {"detail": e.detail},
                    status_code = e.status_code
                    )
            
            except Exception as e:
                logger.debug("HTTP Response: 500 Internal Server Error")
                return JSONResponse(
                    content = {"detail": "Internal Server Error"},
                    status_code = 500,
                )

        return custom_route_handler
