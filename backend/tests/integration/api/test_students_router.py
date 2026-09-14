import pytest
from httpx import AsyncClient

STUDENT_PAYLOAD = {
    "first_name": "Juan",
    "last_name": "Perez",
    "dni": "30123456",
    "date_of_birth": "1995-05-20",
    "phone": "+54 9 11 1234-5678",
    "email": "juan.perez@example.com",
}


@pytest.mark.asyncio
async def test_create_student_success(client: AsyncClient) -> None:
    response = await client.post("/v1/students", json=STUDENT_PAYLOAD)

    assert response.status_code == 201
    data = response.json()
    assert data["dni"] == "30123456"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_student_invalid_dni_returns_422(client: AsyncClient) -> None:
    payload = {**STUDENT_PAYLOAD, "dni": "abc123"}

    response = await client.post("/v1/students", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_student_duplicate_dni_returns_409(client: AsyncClient) -> None:
    await client.post("/v1/students", json=STUDENT_PAYLOAD)

    response = await client.post("/v1/students", json=STUDENT_PAYLOAD)

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_student_not_found_returns_404(client: AsyncClient) -> None:
    response = await client.get(
        "/v1/students/00000000-0000-0000-0000-000000000000"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_students_pagination(client: AsyncClient) -> None:
    for index in range(3):
        payload = {**STUDENT_PAYLOAD, "dni": f"3000000{index}"}
        await client.post("/v1/students", json=payload)

    response = await client.get("/v1/students", params={"limit": 2, "offset": 0})

    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["data"]) == 2


@pytest.mark.asyncio
async def test_update_student_partial(client: AsyncClient) -> None:
    create_response = await client.post("/v1/students", json=STUDENT_PAYLOAD)
    student_id = create_response.json()["id"]

    response = await client.patch(
        f"/v1/students/{student_id}", json={"phone": "+54 11 4444-4444"}
    )

    assert response.status_code == 200
    assert response.json()["phone"] == "+54 11 4444-4444"


@pytest.mark.asyncio
async def test_delete_student_success_and_idempotency(client: AsyncClient) -> None:
    create_response = await client.post("/v1/students", json=STUDENT_PAYLOAD)
    student_id = create_response.json()["id"]

    delete_response = await client.delete(f"/v1/students/{student_id}")
    assert delete_response.status_code == 204

    second_delete = await client.delete(f"/v1/students/{student_id}")
    assert second_delete.status_code == 404


@pytest.mark.asyncio
async def test_get_student_by_dni(client: AsyncClient) -> None:
    await client.post("/v1/students", json=STUDENT_PAYLOAD)

    response = await client.get(f"/v1/students/dni/{STUDENT_PAYLOAD['dni']}")

    assert response.status_code == 200
    assert response.json()["dni"] == STUDENT_PAYLOAD["dni"]
