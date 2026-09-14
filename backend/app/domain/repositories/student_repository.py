from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.student import Student


class StudentRepository(ABC):
    @abstractmethod
    async def save(self, student: Student) -> Student: ...

    @abstractmethod
    async def find_by_id(self, student_id: UUID) -> Student | None: ...

    @abstractmethod
    async def find_by_dni(self, dni: str) -> Student | None: ...

    @abstractmethod
    async def find_all(
        self, limit: int = 50, offset: int = 0
    ) -> tuple[list[Student], int]: ...

    @abstractmethod
    async def update(self, student: Student) -> Student: ...

    @abstractmethod
    async def delete(self, student_id: UUID) -> bool: ...
