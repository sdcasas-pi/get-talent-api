from dataclasses import dataclass
from uuid import UUID

from app.application.dto.student_dto import StudentResultDTO, UpdateStudentDTO
from app.domain.exceptions.student_exceptions import (
    DuplicateDniError,
    StudentNotFoundError,
)
from app.domain.repositories.student_repository import StudentRepository


@dataclass
class UpdateStudentUseCase:
    repository: StudentRepository

    async def execute(
        self, student_id: UUID, dto: UpdateStudentDTO
    ) -> StudentResultDTO:
        student = await self.repository.find_by_id(student_id)
        if student is None:
            raise StudentNotFoundError(str(student_id))

        if dto.dni is not None and dto.dni != student.dni:
            existing = await self.repository.find_by_dni(dto.dni)
            if existing is not None:
                raise DuplicateDniError(dto.dni)
            student.change_dni(dto.dni)

        if dto.first_name is not None:
            student.first_name = dto.first_name
        if dto.last_name is not None:
            student.last_name = dto.last_name
        if dto.date_of_birth is not None:
            student.date_of_birth = dto.date_of_birth
        if dto.phone is not None:
            student.phone = dto.phone
        if dto.email is not None:
            student.email = dto.email

        updated = await self.repository.update(student)
        return StudentResultDTO.from_entity(updated)
