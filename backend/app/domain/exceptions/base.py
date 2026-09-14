class DomainException(Exception):
    """Base for all domain exceptions."""

    def __init__(self, message: str, code: str = "DOMAIN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(self.message)


class EntityNotFoundError(DomainException):
    def __init__(self, entity: str, entity_id: str) -> None:
        super().__init__(
            message=f"{entity} with id '{entity_id}' not found",
            code="ENTITY_NOT_FOUND",
        )
