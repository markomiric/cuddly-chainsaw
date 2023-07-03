import time
from typing import Callable

from fastapi import Request, Response
from fastapi.routing import APIRoute
from starlette.background import BackgroundTask

from src.config import logger


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        """
        Returns a custom route handler function that measures the duration of the route.

        Returns:
            A callable custom route handler function.
        """
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            """
            Custom route handler function that measures the duration of the route.

            Args:
                request (Request): The incoming request object.

            Returns:
                Response: The response object.
            """
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["Response-Time"] = str(duration)
            print(f"Route duration: {duration}")
            return response

        return custom_route_handler


def log_info(request_body, response_body):
    logger.info(request_body.decode())
    logger.info(response_body.decode())
