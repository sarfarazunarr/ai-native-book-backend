from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import settings
from .logging_config import setup_logging
from .vector_db import vector_db
from .api.health import router as health_router
from .api.chat import router as chat_router
from .api.admin import router as admin_router
from .api.home import router as home_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    setup_logging(settings.log_level)
    logger = logging.getLogger(__name__)
    logger.info("Starting up the AI Book Chatbot application")
    
    # Initialize the vector database
    try:
        vector_db.init_collection()
        logger.info("Successfully initialized vector database")
    except Exception as e:
        logger.error(f"Failed to initialize vector database: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down the AI Book Chatbot application")
    vector_db.close_connection()


# Create the FastAPI app with lifespan
app = FastAPI(
    title="AI-Powered Chatbot for Physical AI & Humanoid Robotics Book",
    description="API for interacting with the robotics book chatbot",
    version="1.0.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://physical-ai-humanoid-robotics-omega.vercel.app/"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include API routers
app.include_router(home_router, prefix="/", tags=["home"])
app.include_router(health_router, prefix="", tags=["health"])
app.include_router(chat_router, prefix="", tags=["chat"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )