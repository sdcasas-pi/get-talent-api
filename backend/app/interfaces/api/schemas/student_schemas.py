from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CreateStudentRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "first_name": "Juan",
                    "last_name": "Perez",
                    "dni": "30123456",
                    "date_of_birth": "1995-05-20",
                    "phone": "+549111234-5678",
                    "email": "juan.perez@example.com",
                }
            ]
        }
    )

    first_name: str = Field(
        ..., min_length=1, max_length=100, description="Student first name"
    )
    last_name: str = Field(
        ..., min_length=1, max_length=100, description="Student last name"
    )
    dni: str = Field(
        ..., pattern=r"^\d{7,8}$", description="Argentine DNI, 7 or 8 digits"
    )
    date_of_birth: date = Field(..., description="Date of birth")
    phone: str | None = Field(
        default=None, max_length=30, description="Optional phone number"
    )
    email: str | None = Field(
        default=None,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="Optional email address",
    )


class UpdateStudentRequest(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)
    dni: str | None = Field(default=None, pattern=r"^\d{7,8}$")
    date_of_birth: date | None = None
    phone: str | None = Field(default=None, max_length=30)
    email: str | None = Field(default=None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")


class StudentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    dni: str
    date_of_birth: date
    phone: str | None
    email: str | None
    created_at: datetime


class StudentListResponse(BaseModel):
    data: list[StudentResponse]
    total: int
    limit: int
    offset: int


class ErrorResponse(BaseModel):
    error: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    details: list[str] | None = Field(default=None, description="Additional details")
