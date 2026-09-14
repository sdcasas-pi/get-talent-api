from app.application.dto.student_dto import StudentListResultDTO, StudentResultDTO
from app.interfaces.api.schemas.student_schemas import (
    StudentListResponse,
    StudentResponse,
)


class StudentMapper:
    @staticmethod
    def to_response(dto: StudentResultDTO) -> StudentResponse:
        return StudentResponse(
            id=dto.id,
            first_name=dto.first_name,
            last_name=dto.last_name,
            dni=dto.dni,
            date_of_birth=dto.date_of_birth,
            phone=dto.phone,
            email=dto.email,
            created_at=dto.created_at,
        )

    @staticmethod
    def to_list_response(dto: StudentListResultDTO) -> StudentListResponse:
        return StudentListResponse(
            data=[StudentMapper.to_response(item) for item in dto.items],
            total=dto.total,
            limit=dto.limit,
            offset=dto.offset,
        )
