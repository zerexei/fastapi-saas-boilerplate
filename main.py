from fastapi import FastAPI

from config import settings
from core.exceptions import register_exception_handlers
from core.lifespan import lifespan
from core.logger import configure_logging, get_logger
from core.middleware import register_middlewares
from domains.users.router import router as users_router

configure_logging()
logger = get_logger(__name__)


def create_application() -> FastAPI:
    """FastAPI application factory pattern."""
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="FastAPI starter template using a modular monolith layout, domain-driven design, and multi-tenant isolation.",
        lifespan=lifespan,
    )

    register_middlewares(app)
    register_exception_handlers(app)
    _register_routes(app)
    return app


def _register_routes(app: FastAPI) -> None:
    app.include_router(users_router, prefix="/api/v1", tags=["users"])

    @app.get("/health", tags=["Health"])
    async def health_check():
        """Service health check endpoint."""
        return {"status": "healthy", "service": "operational"}


app = create_application()
