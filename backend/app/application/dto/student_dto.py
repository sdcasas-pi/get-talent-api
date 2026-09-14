from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from app.domain.entities.student import Student


@dataclass(frozen=True)
class CreateStudentDTO:
    first_name: str
    last_name: str
    dni: str
    date_of_birth: date
    phone: str | None = None
    email: str | None = None


@dataclass(frozen=True)
class UpdateStudentDTO:
    first_name: str | None = None
    last_name: str | None = None
    dni: str | None = None
    date_of_birth: date | None = None
    phone: str | None = None
    email: str | None = None


@dataclass(frozen=True)
class StudentResultDTO:
    id: UUID
    first_name: str
    last_name: str
    dni: str
    date_of_birth: date
    phone: str | None
    email: str | None
    created_at: datetime

    @classmethod
    def from_entity(cls, entity: Student) -> "StudentResultDTO":
        return cls(
            id=entity.id,
            first_name=entity.first_name,
            last_name=entity.last_name,
            dni=entity.dni,
            date_of_birth=entity.date_of_birth,
            phone=entity.phone,
            email=entity.email,
            created_at=entity.created_at,
        )


@dataclass(frozen=True)
class StudentListResultDTO:
    items: list[StudentResultDTO]
    total: int
    limit: int
    offset: int
