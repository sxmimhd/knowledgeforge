from contextlib import asynccontextmanager

from fastapi import FastAPI

import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting KnowledgeForge API...")

    # Future startup tasks:
    # - Connect PostgreSQL
    # - Connect Qdrant
    # - Load embedding models
    # - Verify Ollama/OpenAI
    # - Create upload directories

    yield

    logger.info("Shutting down KnowledgeForge API...")

    # Future shutdown tasks:
    # - Close database connections
    # - Flush caches
    # - Stop background workers