import re
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from app.domain.exceptions.student_exceptions import InvalidDniError

_DNI_PATTERN = re.compile(r"^\d{7,8}$")


@dataclass
class Student:
    first_name: str
    last_name: str
    dni: str
    date_of_birth: date
    id: UUID = field(default_factory=uuid4)
    phone: str | None = None
    email: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not _DNI_PATTERN.match(self.dni):
            raise InvalidDniError(self.dni)

    def change_dni(self, new_dni: str) -> None:
        if not _DNI_PATTERN.match(new_dni):
            raise InvalidDniError(new_dni)
        self.dni = new_dni
