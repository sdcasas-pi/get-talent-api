from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.student import Student
from app.domain.repositories.student_repository import StudentRepository
from app.infrastructure.persistence.sqlalchemy.models import StudentModel


class SqlAlchemyStudentRepository(StudentRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, student: Student) -> Student:
        model = self._to_model(student)
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, student_id: UUID) -> Student | None:
        model = await self._session.get(StudentModel, student_id)
        return self._to_entity(model) if model else None

    async def find_by_dni(self, dni: str) -> Student | None:
        result = await self._session.execute(
            select(StudentModel).where(StudentModel.dni == dni)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_all(
        self, limit: int = 50, offset: int = 0
    ) -> tuple[list[Student], int]:
        total_result = await self._session.execute(
            select(func.count(StudentModel.id))
        )
        total = total_result.scalar_one()

        result = await self._session.execute(
            select(StudentModel)
            .order_by(StudentModel.last_name, StudentModel.first_name)
            .limit(limit)
            .offset(offset)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models], total

    async def update(self, student: Student) -> Student:
        model = await self._session.get(StudentModel, student.id)
        if model is None:
            model = self._to_model(student)
            self._session.add(model)
        else:
            model.first_name = student.first_name
            model.last_name = student.last_name
            model.dni = student.dni
            model.date_of_birth = student.date_of_birth
            model.phone = student.phone
            model.email = student.email
        await self._session.commit()
        await self._session.refresh(model)
        return self._to_entity(model)

    async def delete(self, student_id: UUID) -> bool:
        model = await self._session.get(StudentModel, student_id)
        if model is None:
            return False
        await self._session.delete(model)
        await self._session.commit()
        return True

    @staticmethod
    def _to_model(student: Student) -> StudentModel:
        return StudentModel(
            id=student.id,
            first_name=student.first_name,
            last_name=student.last_name,
            dni=student.dni,
            date_of_birth=student.date_of_birth,
            phone=student.phone,
            email=student.email,
        )

    @staticmethod
    def _to_entity(model: StudentModel) -> Student:
        student = Student(
            first_name=model.first_name,
            last_name=model.last_name,
            dni=model.dni,
            date_of_birth=model.date_of_birth,
            id=model.id,
            phone=model.phone,
            email=model.email,
        )
        student.created_at = model.created_at
        return student
