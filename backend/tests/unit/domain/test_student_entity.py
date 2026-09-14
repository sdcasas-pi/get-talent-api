from datetime import date

import pytest

from app.domain.entities.student import Student
from app.domain.exceptions.student_exceptions import InvalidDniError

_DEFAULT_DOB = date(1995, 5, 20)


def _build_student(
    dni: str = "30123456",
    first_name: str = "Juan",
    last_name: str = "Perez",
    date_of_birth: date = _DEFAULT_DOB,
) -> Student:
    return Student(
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        date_of_birth=date_of_birth,
    )


def test_create_student_with_valid_dni() -> None:
    student = _build_student()
    assert student.dni == "30123456"
    assert student.id is not None


def test_create_student_with_invalid_dni_raises() -> None:
    with pytest.raises(InvalidDniError):
        _build_student(dni="abc")


def test_change_dni_updates_value() -> None:
    student = _build_student()
    student.change_dni("40111222")
    assert student.dni == "40111222"


def test_change_dni_with_invalid_value_raises() -> None:
    student = _build_student()
    with pytest.raises(InvalidDniError):
        student.change_dni("not-a-dni")
