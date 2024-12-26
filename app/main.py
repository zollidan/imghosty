import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from fastapi.staticfiles import StaticFiles
from app.api.router import router
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting appication...")
    yield
    logging.info("Shutting down appication...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.mount("/files", StaticFiles(directory=settings.UPLOAD_DIR), name="files")
