from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.infrastructure.config.settings import Settings
from app.infrastructure.persistence.sqlalchemy.base import Base, build_engine
from app.interfaces.api.dependencies import get_settings
from app.interfaces.api.exception_handlers import register_exception_handlers
from app.interfaces.api.v1.students_router import router as students_router

CORRELATION_HEADER = "X-Correlation-ID"


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        cid = request.headers.get(CORRELATION_HEADER, str(uuid4()))
        response = await call_next(request)
        response.headers[CORRELATION_HEADER] = cid
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    engine = build_engine(settings.database_url)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


def _register_middleware(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(CorrelationIdMiddleware)


def _include_routers(app: FastAPI) -> None:
    app.include_router(students_router)

    @app.get("/health", tags=["System"], summary="Health check")
    async def health_check() -> dict[str, str]:
        settings = get_settings()
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Student Registration Service",
        version=settings.app_version,
        description="API for registering and managing students in a course.",
        lifespan=lifespan,
    )

    _register_middleware(app, settings)
    register_exception_handlers(app)
    _include_routers(app)

    return app


app = create_app()
