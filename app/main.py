import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Starting appication...")
    yield
    logging.info("Shutting down appication...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)
