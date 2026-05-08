import structlog
import logging
from fastapi import Request
from typing import Callable, Awaitable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

def setup_logging() -> None:
    """Configures structured JSON logging optimized for external observability platforms."""
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    logging.basicConfig(format="%(message)s", level=logging.INFO)

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log every incoming request and outgoing response."""
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        logger = structlog.get_logger()
        logger.info("request_started", method=request.method, path=request.url.path)
        try:
            response = await call_next(request)
            logger.info("request_finished", method=request.method, path=request.url.path, status_code=response.status_code)
            return response
        except Exception as e:
            logger.exception("request_failed", method=request.method, path=request.url.path, error=str(e))
            raise
