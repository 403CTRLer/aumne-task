from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import init_db
from .routes import appointments
from .scheduler import shutdown_scheduler, start_scheduler


def create_app(*, enable_scheduler: bool = True, initialize_database: bool = True) -> FastAPI:
    """Compose the FastAPI application with routing, middleware, and lifecycle."""

    settings = get_settings()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Initialize shared resources on startup and release them on shutdown."""

        if initialize_database:
            init_db()
        if enable_scheduler:
            start_scheduler()
        yield
        if enable_scheduler:
            shutdown_scheduler()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(appointments.router)

    return app


app = create_app()

