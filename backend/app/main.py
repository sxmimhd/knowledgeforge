import logging

from fastapi import FastAPI

from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    description="""
    Enterprise RAG Knowledge Platform

    Production-ready AI knowledge assistant supporting:

    • Document Upload
    • Semantic Search
    • Streaming Chat
    • Citations
    • Workspace Management
    """,
    version=settings.app_version,
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }