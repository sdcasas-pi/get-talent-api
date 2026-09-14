from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.infrastructure.persistence.memory.in_memory_student_repository import (
    InMemoryStudentRepository,
)
from app.interfaces.api.dependencies import get_student_repository
from app.main import create_app


@pytest.fixture
def student_repository() -> InMemoryStudentRepository:
    return InMemoryStudentRepository()


@pytest.fixture
def app(student_repository: InMemoryStudentRepository) -> FastAPI:
    application = create_app()
    application.dependency_overrides[get_student_repository] = (
        lambda: student_repository
    )
    return application


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
