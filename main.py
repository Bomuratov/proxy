import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from router import router



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


origins = ["*"]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting system")
    yield
    logger.info("Closing system") 


fapp = FastAPI(debug=True)
fapp.include_router(router)