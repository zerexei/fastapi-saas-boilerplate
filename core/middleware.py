import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Injects a unique tracing Request ID and calculates execution duration

    for every HTTP request passing through the application.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Check if client sent an ID, otherwise generate a new UUID4 trace ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Attach request_id to request state for access in logs or endpoints
        request.state.request_id = request_id

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Inject telemetry headers into the HTTP response
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        return response
