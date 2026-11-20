from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.exceptions import register_exception_handlers
from app.middleware import register_middlewares
from config.settings import settings
from utils.logging_config import setup_logging

setup_logging()
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
register_middlewares(app)
register_exception_handlers(app)
app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": settings.VERSION,
    }
