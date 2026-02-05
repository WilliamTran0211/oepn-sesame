import logging
import traceback
from httpx import Request
from app.schemas.request import ErrorLog, RequestInfo, RequestLog, RequestLog

logger = logging.getLogger("open_sesame_logger")


def log_request(request: Request):
    request_info = RequestInfo(request)
    request_log = RequestLog(
        req_id=request.state.req_id,
        method=request_info.method,
        route=request_info.route,
        ip=request_info.ip,
        url=request_info.url,
        host=request_info.host,
        body=request_info.body,
        headers=request_info.headers,
    )
    logger.info(request_log.model_dump())


def log_error(uuid: str, response_body: dict):
    error_log = ErrorLog(
        req_id=uuid,
        error_message=response_body["error_message"],
    )
    logger.error(error_log.model_dump())
    logger.error(traceback.format_exc())

