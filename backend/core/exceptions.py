from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import structlog

logger = structlog.get_logger()

class DomainException(Exception):
    """Base class for all domain-specific exceptions."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    """Catches all DomainExceptions and returns a standardized JSON response."""
    logger.error("domain_exception", message=exc.message, path=request.url.path, status_code=exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"message": exc.message, "type": "domain_error"}}
    )

def setup_exception_handlers(app: FastAPI) -> None:
    """Registers custom exception handlers with the FastAPI app."""
    app.add_exception_handler(DomainException, domain_exception_handler)
