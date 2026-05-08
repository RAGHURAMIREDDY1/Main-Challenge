from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import get_settings
from backend.core.logging import setup_logging, LoggingMiddleware
from backend.core.exceptions import setup_exception_handlers
from backend.api.api_v1.api import api_router
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse

# Initialize settings
settings = get_settings()

# Initialize structured logging
setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration (Security)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add Middleware
app.add_middleware(LoggingMiddleware)

# Mock Rate Limit Middleware (Security & Scalability)
class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # In a real app, check Redis for IP/Token limits
        # if rate_limit_exceeded: return JSONResponse(status_code=429, content={"error": "Too many requests"})
        return await call_next(request)

app.add_middleware(RateLimitMiddleware)

# Setup centralized error handlers
setup_exception_handlers(app)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    # Local development server
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
