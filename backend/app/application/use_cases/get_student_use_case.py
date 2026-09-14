from dataclasses import dataclass
from uuid import UUID

from app.application.dto.student_dto import StudentResultDTO
from app.domain.exceptions.student_exceptions import StudentNotFoundError
from app.domain.repositories.student_repository import StudentRepository


@dataclass
class GetStudentUseCase:
    repository: StudentRepository

    async def execute(self, student_id: UUID) -> StudentResultDTO:
        student = await self.repository.find_by_id(student_id)
        if student is None:
            raise StudentNotFoundError(str(student_id))
        return StudentResultDTO.from_entity(student)
