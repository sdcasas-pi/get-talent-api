from dataclasses import dataclass
from uuid import UUID

from app.domain.exceptions.student_exceptions import StudentNotFoundError
from app.domain.repositories.student_repository import StudentRepository


@dataclass
class DeleteStudentUseCase:
    repository: StudentRepository

    async def execute(self, student_id: UUID) -> None:
        deleted = await self.repository.delete(student_id)
        if not deleted:
            raise StudentNotFoundError(str(student_id))
