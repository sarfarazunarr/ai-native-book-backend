from typing import Optional
from fastapi import HTTPException, status
import logging


logger = logging.getLogger(__name__)


class BaseAppException(Exception):
    """Base application exception class."""
    
    def __init__(self, message: str, cause: Optional[Exception] = None):
        super().__init__(message)
        self.message = message
        self.cause = cause
        logger.error(f"{self.__class__.__name__}: {message}", exc_info=cause)


class ConfigurationError(BaseAppException):
    """Raised when there's an issue with application configuration."""
    pass


class VectorDBError(BaseAppException):
    """Raised when there's an issue with vector database operations."""
    pass


class ContentIngestionError(BaseAppException):
    """Raised when there's an issue with content ingestion."""
    pass


class AgentError(BaseAppException):
    """Raised when there's an issue with agent operations."""
    pass


class ValidationError(BaseAppException):
    """Raised when there's a validation error."""
    pass


# HTTP Exceptions for API endpoints
class HTTPNotFoundError(HTTPException):
    """HTTP 404 exception."""
    
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class HTTPBadRequestError(HTTPException):
    """HTTP 400 exception."""
    
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class HTTPUnauthorizedError(HTTPException):
    """HTTP 401 exception."""
    
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class HTTPInternalServerError(HTTPException):
    """HTTP 500 exception."""
    
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)


# Exception handlers for FastAPI
def add_exception_handlers(app):
    """Add exception handlers to the FastAPI app."""
    
    @app.exception_handler(BaseAppException)
    async def handle_base_app_exception(request, exc):
        logger.error(f"Application error: {exc.message}", exc_info=exc.cause)
        return HTTPInternalServerError(detail=exc.message)
    
    @app.exception_handler(HTTPException)
    async def handle_http_exception(request, exc):
        logger.warning(f"HTTP error: {exc.status_code} - {exc.detail}")
        return exc