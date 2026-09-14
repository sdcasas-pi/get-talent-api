from app.domain.exceptions.base import DomainException, EntityNotFoundError


class StudentNotFoundError(EntityNotFoundError):
    def __init__(self, student_id: str) -> None:
        super().__init__(entity="Student", entity_id=student_id)


class DuplicateDniError(DomainException):
    def __init__(self, dni: str) -> None:
        super().__init__(
            message=f"A student with dni '{dni}' already exists",
            code="DUPLICATE_DNI",
        )


class InvalidDniError(DomainException):
    def __init__(self, dni: str) -> None:
        super().__init__(
            message=f"Invalid dni format: '{dni}'",
            code="INVALID_DNI",
        )
