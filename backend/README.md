# Student Registration Service

Backend FastAPI para el registro y administración de alumnos de un curso/capacitación. Implementado con **Clean Architecture** (domain / application / infrastructure / interfaces), async-first y Pydantic v2.

## Stack

| Componente | Tecnología |
|---|---|
| Framework | FastAPI |
| Servidor ASGI | Uvicorn |
| Validación | Pydantic v2 |
| ORM | SQLAlchemy 2.0 (async) |
| Base de datos | SQLite (`aiosqlite`) |
| Tests | pytest + pytest-asyncio + httpx |
| Lint / Types | ruff, mypy (strict), black |

## Arquitectura

```
app/
├── main.py                    # Application factory (create_app)
├── domain/                    # Entidades, excepciones y contratos de repositorio (sin dependencias externas)
│   ├── entities/student.py
│   ├── exceptions/
│   └── repositories/student_repository.py
├── application/                # Casos de uso y DTOs (orquestación, sin reglas de negocio propias)
│   ├── dto/student_dto.py
│   └── use_cases/
├── infrastructure/             # Adaptadores: DB, settings, logging
│   ├── config/settings.py
│   ├── logging/logger.py
│   └── persistence/
│       ├── sqlalchemy/         # Implementación real (SQLite)
│       └── memory/             # Implementación en memoria (tests)
└── interfaces/                 # HTTP: routers, schemas Pydantic, mappers, DI
    ├── api/
    │   ├── schemas/student_schemas.py
    │   ├── dependencies.py     # Composition root (Depends())
    │   ├── exception_handlers.py
    │   └── v1/students_router.py
    └── mappers/student_mapper.py

tests/
├── unit/          # Dominio y casos de uso (repositorio en memoria)
└── integration/   # Endpoints vía httpx.AsyncClient
```

Regla de dependencia: `Interfaces → Application → Domain`, con `Infrastructure` implementando las interfaces del dominio e inyectándose vía `Depends()`. El dominio no importa ningún framework.

## Requisitos

- Python 3.12+

## Instalación

```bash
cd backend
# activá tu entorno virtual de Python 3.12 antes de este paso
pip install -r requirements-dev.txt
cp .env.example .env
```

## Configuración (`.env`)

| Variable | Default | Descripción |
|---|---|---|
| `APP_NAME` | `student-registration-service` | Nombre del servicio |
| `DEBUG` | `false` | Modo debug |
| `DATABASE_URL` | `sqlite+aiosqlite:///./students.db` | URL de conexión async a la base de datos |

## Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health check: `GET /health`

## Endpoints

Base path: `/v1/students`

| Método | Path | Descripción |
|---|---|---|
| `POST` | `/v1/students` | Registra un nuevo alumno (201) |
| `GET` | `/v1/students` | Lista alumnos paginada (`limit`, `offset`) |
| `GET` | `/v1/students/{id}` | Obtiene un alumno por ID |
| `GET` | `/v1/students/dni/{dni}` | Obtiene un alumno por DNI |
| `PATCH` | `/v1/students/{id}` | Actualiza campos parcialmente |
| `DELETE` | `/v1/students/{id}` | Elimina un alumno (204) |

### Modelo `Student`

| Campo | Tipo | Requerido | Validación |
|---|---|---|---|
| `first_name` | string | Sí | 1-100 caracteres |
| `last_name` | string | Sí | 1-100 caracteres |
| `dni` | string | Sí, único | 7 u 8 dígitos numéricos |
| `date_of_birth` | date (`YYYY-MM-DD`) | Sí | — |
| `phone` | string | No | máx. 30 caracteres |
| `email` | string | No | formato email |

### Ejemplo — crear alumno

```bash
curl -X POST http://127.0.0.1:8000/v1/students \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Juan",
    "last_name": "Perez",
    "dni": "30123456",
    "date_of_birth": "1995-05-20",
    "phone": "+54 9 11 1234-5678",
    "email": "juan.perez@example.com"
  }'
```

### Códigos de error

| Código HTTP | Cuándo |
|---|---|
| `404` | Alumno no encontrado |
| `409` | DNI duplicado |
| `422` | Error de validación (DNI/email con formato inválido, campos faltantes) |
| `500` | Error interno no controlado |

## Colección de Postman

En `../postman/` (a la altura de `backend/` y `frontend/`) están la colección y el environment listos para importar:

- `postman/student-registration.postman_collection.json`
- `postman/student-registration.postman_environment.json`

Incluye los 7 endpoints (Health + CRUD de Students) y un script en **Create Student** que guarda automáticamente `student_id`/`student_dni` como variables de colección para encadenar el resto de los requests sin copiar/pegar el id manualmente.

## Testing

```bash
pytest                 # corre toda la suite con cobertura (mínimo 85%)
pytest tests/unit       # solo unit tests (dominio + casos de uso, repo en memoria)
pytest tests/integration  # solo tests de API (httpx.AsyncClient)
```

## Calidad de código

```bash
ruff check .            # lint
mypy app                # type-check estricto
black .                 # formateo
```

## Notas de diseño

- **Persistencia intercambiable**: `StudentRepository` es una interfaz de dominio; hoy la implementa `SqlAlchemyStudentRepository` sobre SQLite, pero se puede migrar a Postgres u otro motor sin tocar `domain/` ni `application/`.
- **Sin autenticación** por ahora — el punto de extensión ya existe (`Depends()` en `interfaces/api/dependencies.py`) para agregar JWT/API Key sin refactor.
- **Baja lógica en el borrado**: es un hard delete; si se necesita soft delete o auditoría de bajas, se agrega como campo en la entidad y el modelo ORM.

## Pendiente / fuera de alcance del MVP

- Diagrama de arquitectura (`docs/architecture.md`)
- Autenticación (JWT/API Key)
- Migraciones con Alembic (hoy las tablas se crean automáticamente en el `lifespan` de arranque, apto para desarrollo)
