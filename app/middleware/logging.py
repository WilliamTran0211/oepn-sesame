import json
import uuid
import logging
from contextvars import ContextVar
from fastapi import HTTPException, Request
from fastapi.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware
from app.logger.utils import log_error, log_request

logger = logging.getLogger(__name__)

request_id_var = ContextVar("request_id", default=None)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())
        try:
            #### request ####
            request.state.req_id = req_id
            request.state.body = json.loads(await request.body() or "{}")
            log_request(request)

            #### response ####
            response = await call_next(request)
            response_body = ""
            if response.headers.get("content-type") == "application/json":
                response_body = [chunk async for chunk in response.body_iterator]
                response.body_iterator = iterate_in_threadpool(iter(response_body))
            return response

        except Exception as e:
            # Unexpected error handling
            log_error(req_id, {"error_message": "ERR_UNEXPECTED"})
            return HTTPException(status_code=500, detail="ERR_UNEXPECTED")
