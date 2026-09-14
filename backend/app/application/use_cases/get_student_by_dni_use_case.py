from dataclasses import dataclass

from app.application.dto.student_dto import StudentResultDTO
from app.domain.exceptions.student_exceptions import StudentNotFoundError
from app.domain.repositories.student_repository import StudentRepository


@dataclass
class GetStudentByDniUseCase:
    repository: StudentRepository

    async def execute(self, dni: str) -> StudentResultDTO:
        student = await self.repository.find_by_dni(dni)
        if student is None:
            raise StudentNotFoundError(dni)
        return StudentResultDTO.from_entity(student)
