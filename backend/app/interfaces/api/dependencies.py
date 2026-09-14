from collections.abc import AsyncIterator
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.application.use_cases.create_student_use_case import CreateStudentUseCase
from app.application.use_cases.delete_student_use_case import DeleteStudentUseCase
from app.application.use_cases.get_student_by_dni_use_case import (
    GetStudentByDniUseCase,
)
from app.application.use_cases.get_student_use_case import GetStudentUseCase
from app.application.use_cases.list_students_use_case import ListStudentsUseCase
from app.application.use_cases.update_student_use_case import UpdateStudentUseCase
from app.domain.repositories.student_repository import StudentRepository
from app.infrastructure.config.settings import Settings
from app.infrastructure.persistence.sqlalchemy.base import (
    build_engine,
    build_session_factory,
)
from app.infrastructure.persistence.sqlalchemy.sqlalchemy_student_repository import (
    SqlAlchemyStudentRepository,
)


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    engine = build_engine(get_settings().database_url)
    return build_session_factory(engine)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    session_factory = _get_session_factory()
    async with session_factory() as session:
        yield session


def get_student_repository(
    session: AsyncSession = Depends(get_db_session),
) -> StudentRepository:
    return SqlAlchemyStudentRepository(session=session)


def get_create_student_use_case(
    repository: StudentRepository = Depends(get_student_repository),
) -> CreateStudentUseCase:
    return CreateStudentUseCase(repository=repository)


def get_student_use_case(
    repository: StudentRepository = Depends(get_student_repository),
) -> GetStudentUseCase:
    return GetStudentUseCase(repository=repository)


def get_student_by_dni_use_case(
    repository: StudentRepository = Depends(get_student_repository),
) -> GetStudentByDniUseCase:
    return GetStudentByDniUseCase(repository=repository)


def get_list_students_use_case(
    repository: StudentRepository = Depends(get_student_repository),
) -> ListStudentsUseCase:
    return ListStudentsUseCase(repository=repository)


def get_update_student_use_case(
    repository: StudentRepository = Depends(get_student_repository),
) -> UpdateStudentUseCase:
    return UpdateStudentUseCase(repository=repository)


def get_delete_student_use_case(
    repository: StudentRepository = Depends(get_student_repository),
) -> DeleteStudentUseCase:
    return DeleteStudentUseCase(repository=repository)
