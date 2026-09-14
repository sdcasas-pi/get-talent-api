from dataclasses import dataclass

from app.application.dto.student_dto import StudentListResultDTO, StudentResultDTO
from app.domain.repositories.student_repository import StudentRepository


@dataclass
class ListStudentsUseCase:
    repository: StudentRepository

    async def execute(self, limit: int = 50, offset: int = 0) -> StudentListResultDTO:
        students, total = await self.repository.find_all(limit=limit, offset=offset)
        return StudentListResultDTO(
            items=[StudentResultDTO.from_entity(student) for student in students],
            total=total,
            limit=limit,
            offset=offset,
        )
