import logging
import time
import traceback
import uuid
from contextvars import ContextVar

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("open_sesame_logger")

request_id_var = ContextVar("request_id", default=None)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())
        request.state.req_id = req_id
        start = time.perf_counter()

        logger.info(
            {
                "req_id": req_id,
                "method": request.method,
                "path": request.url.path,
                "ip": request.client.host if request.client else None,
                "user_agent": request.headers.get("user-agent"),
            }
        )

        try:
            response = await call_next(request)
        except Exception:
            logger.error(
                {
                    "req_id": req_id,
                    "error": "unhandled_exception",
                    "traceback": traceback.format_exc(),
                }
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error": "server_error",
                    "error_description": "An unexpected error occurred.",
                },
            )

        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            {
                "req_id": req_id,
                "status_code": response.status_code,
                "duration_ms": round(duration_ms, 2),
            }
        )

        response.headers["X-Request-ID"] = req_id
        return response
