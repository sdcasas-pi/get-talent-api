from uuid import UUID

from fastapi import APIRouter, Depends, Query, status

from app.application.dto.student_dto import CreateStudentDTO, UpdateStudentDTO
from app.application.use_cases.create_student_use_case import CreateStudentUseCase
from app.application.use_cases.delete_student_use_case import DeleteStudentUseCase
from app.application.use_cases.get_student_by_dni_use_case import (
    GetStudentByDniUseCase,
)
from app.application.use_cases.get_student_use_case import GetStudentUseCase
from app.application.use_cases.list_students_use_case import ListStudentsUseCase
from app.application.use_cases.update_student_use_case import UpdateStudentUseCase
from app.interfaces.api.dependencies import (
    get_create_student_use_case,
    get_delete_student_use_case,
    get_list_students_use_case,
    get_student_by_dni_use_case,
    get_student_use_case,
    get_update_student_use_case,
)
from app.interfaces.api.schemas.student_schemas import (
    CreateStudentRequest,
    ErrorResponse,
    StudentListResponse,
    StudentResponse,
    UpdateStudentRequest,
)
from app.interfaces.mappers.student_mapper import StudentMapper

router = APIRouter(prefix="/v1/students", tags=["Students"])


@router.post(
    "",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new student",
    description="Creates a new student registration for the course.",
    responses={
        409: {
            "model": ErrorResponse,
            "description": "A student with this DNI already exists",
        },
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def create_student(
    request: CreateStudentRequest,
    use_case: CreateStudentUseCase = Depends(get_create_student_use_case),
) -> StudentResponse:
    dto = CreateStudentDTO(
        first_name=request.first_name,
        last_name=request.last_name,
        dni=request.dni,
        date_of_birth=request.date_of_birth,
        phone=request.phone,
        email=request.email,
    )
    result = await use_case.execute(dto)
    return StudentMapper.to_response(result)


@router.get(
    "",
    response_model=StudentListResponse,
    summary="List students",
    description="Returns a paginated list of registered students.",
)
async def list_students(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    use_case: ListStudentsUseCase = Depends(get_list_students_use_case),
) -> StudentListResponse:
    result = await use_case.execute(limit=limit, offset=offset)
    return StudentMapper.to_list_response(result)


@router.get(
    "/dni/{dni}",
    response_model=StudentResponse,
    summary="Get student by DNI",
    description="Retrieves a single student by their DNI.",
    responses={404: {"model": ErrorResponse, "description": "Student not found"}},
)
async def get_student_by_dni(
    dni: str,
    use_case: GetStudentByDniUseCase = Depends(get_student_by_dni_use_case),
) -> StudentResponse:
    result = await use_case.execute(dni)
    return StudentMapper.to_response(result)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student by ID",
    description="Retrieves a single student by their unique identifier.",
    responses={404: {"model": ErrorResponse, "description": "Student not found"}},
)
async def get_student(
    student_id: UUID,
    use_case: GetStudentUseCase = Depends(get_student_use_case),
) -> StudentResponse:
    result = await use_case.execute(student_id)
    return StudentMapper.to_response(result)


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update a student",
    description="Partially updates an existing student's data.",
    responses={
        404: {"model": ErrorResponse, "description": "Student not found"},
        409: {
            "model": ErrorResponse,
            "description": "A student with this DNI already exists",
        },
        422: {"model": ErrorResponse, "description": "Validation error"},
    },
)
async def update_student(
    student_id: UUID,
    request: UpdateStudentRequest,
    use_case: UpdateStudentUseCase = Depends(get_update_student_use_case),
) -> StudentResponse:
    dto = UpdateStudentDTO(
        first_name=request.first_name,
        last_name=request.last_name,
        dni=request.dni,
        date_of_birth=request.date_of_birth,
        phone=request.phone,
        email=request.email,
    )
    result = await use_case.execute(student_id, dto)
    return StudentMapper.to_response(result)


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student",
    description="Removes a student registration.",
    responses={404: {"model": ErrorResponse, "description": "Student not found"}},
)
async def delete_student(
    student_id: UUID,
    use_case: DeleteStudentUseCase = Depends(get_delete_student_use_case),
) -> None:
    await use_case.execute(student_id)
