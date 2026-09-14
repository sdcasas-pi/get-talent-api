from datetime import date
from uuid import uuid4

import pytest

from app.application.dto.student_dto import CreateStudentDTO, UpdateStudentDTO
from app.application.use_cases.create_student_use_case import CreateStudentUseCase
from app.application.use_cases.delete_student_use_case import DeleteStudentUseCase
from app.application.use_cases.get_student_use_case import GetStudentUseCase
from app.application.use_cases.list_students_use_case import ListStudentsUseCase
from app.application.use_cases.update_student_use_case import UpdateStudentUseCase
from app.domain.exceptions.student_exceptions import (
    DuplicateDniError,
    StudentNotFoundError,
)
from app.infrastructure.persistence.memory.in_memory_student_repository import (
    InMemoryStudentRepository,
)


def _create_dto(dni: str = "30123456") -> CreateStudentDTO:
    return CreateStudentDTO(
        first_name="Juan",
        last_name="Perez",
        dni=dni,
        date_of_birth=date(1995, 5, 20),
    )


@pytest.mark.asyncio
async def test_create_student_success() -> None:
    repository = InMemoryStudentRepository()
    use_case = CreateStudentUseCase(repository=repository)

    result = await use_case.execute(_create_dto())

    assert result.dni == "30123456"
    assert result.first_name == "Juan"


@pytest.mark.asyncio
async def test_create_student_duplicate_dni_raises() -> None:
    repository = InMemoryStudentRepository()
    use_case = CreateStudentUseCase(repository=repository)
    await use_case.execute(_create_dto())

    with pytest.raises(DuplicateDniError):
        await use_case.execute(_create_dto())


@pytest.mark.asyncio
async def test_get_student_not_found_raises() -> None:
    repository = InMemoryStudentRepository()
    use_case = GetStudentUseCase(repository=repository)

    with pytest.raises(StudentNotFoundError):
        await use_case.execute(uuid4())


@pytest.mark.asyncio
async def test_list_students_returns_paginated_results() -> None:
    repository = InMemoryStudentRepository()
    create_use_case = CreateStudentUseCase(repository=repository)
    for index in range(3):
        await create_use_case.execute(_create_dto(dni=f"3000000{index}"))

    list_use_case = ListStudentsUseCase(repository=repository)
    result = await list_use_case.execute(limit=2, offset=0)

    assert result.total == 3
    assert len(result.items) == 2


@pytest.mark.asyncio
async def test_update_student_partial_fields() -> None:
    repository = InMemoryStudentRepository()
    created = await CreateStudentUseCase(repository=repository).execute(
        _create_dto()
    )
    use_case = UpdateStudentUseCase(repository=repository)

    result = await use_case.execute(
        created.id, UpdateStudentDTO(phone="+54 11 5555-5555")
    )

    assert result.phone == "+54 11 5555-5555"
    assert result.first_name == "Juan"


@pytest.mark.asyncio
async def test_update_student_duplicate_dni_raises() -> None:
    repository = InMemoryStudentRepository()
    await CreateStudentUseCase(repository=repository).execute(
        _create_dto(dni="30123456")
    )
    second = await CreateStudentUseCase(repository=repository).execute(
        _create_dto(dni="40111222")
    )
    use_case = UpdateStudentUseCase(repository=repository)

    with pytest.raises(DuplicateDniError):
        await use_case.execute(second.id, UpdateStudentDTO(dni="30123456"))


@pytest.mark.asyncio
async def test_delete_student_success_and_idempotency() -> None:
    repository = InMemoryStudentRepository()
    created = await CreateStudentUseCase(repository=repository).execute(
        _create_dto()
    )
    use_case = DeleteStudentUseCase(repository=repository)

    await use_case.execute(created.id)

    with pytest.raises(StudentNotFoundError):
        await use_case.execute(created.id)
