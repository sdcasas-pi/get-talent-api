from uuid import UUID

from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository


class InMemoryStudentRepository(StudentRepository):
    def __init__(self) -> None:
        self._store: dict[UUID, Student] = {}

    async def save(self, student: Student) -> Student:
        self._store[student.id] = student
        return student

    async def find_by_id(self, student_id: UUID) -> Student | None:
        return self._store.get(student_id)

    async def find_by_dni(self, dni: str) -> Student | None:
        for student in self._store.values():
            if student.dni == dni:
                return student
        return None

    async def find_all(
        self, limit: int = 50, offset: int = 0
    ) -> tuple[list[Student], int]:
        students = sorted(
            self._store.values(),
            key=lambda student: (student.last_name, student.first_name),
        )
        total = len(students)
        return students[offset : offset + limit], total

    async def update(self, student: Student) -> Student:
        self._store[student.id] = student
        return student

    async def delete(self, student_id: UUID) -> bool:
        if student_id in self._store:
            del self._store[student_id]
            return True
        return False
