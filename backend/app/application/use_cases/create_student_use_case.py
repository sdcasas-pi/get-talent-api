from dataclasses import dataclass

from app.application.dto.student_dto import CreateStudentDTO, StudentResultDTO
from app.domain.entities.student import Student
from app.domain.exceptions.student_exceptions import DuplicateDniError
from app.domain.repositories.student_repository import StudentRepository


@dataclass
class CreateStudentUseCase:
    repository: StudentRepository

    async def execute(self, dto: CreateStudentDTO) -> StudentResultDTO:
        existing = await self.repository.find_by_dni(dto.dni)
        if existing is not None:
            raise DuplicateDniError(dto.dni)

        student = Student(
            first_name=dto.first_name,
            last_name=dto.last_name,
            dni=dto.dni,
            date_of_birth=dto.date_of_birth,
            phone=dto.phone,
            email=dto.email,
        )
        saved = await self.repository.save(student)
        return StudentResultDTO.from_entity(saved)
