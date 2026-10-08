import logging

from fastapi import FastAPI
from app.api.v1 import rag
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import Base, engine
from app.db import models
from app.api.v1 import workspaces
from app.api.v1 import documents

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
Base.metadata.create_all(bind=engine)
app.include_router(api_router)
app.include_router(rag.router, prefix="/api/v1")
app.include_router(
    workspaces.router,
    prefix="/api/v1",
)
app.include_router(
    documents.router,
    prefix="/api/v1",
)

@app.get("/")
def root():
    logger.info("Root endpoint accessed")

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
    }