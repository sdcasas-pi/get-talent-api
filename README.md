# Get Talent

Sistema de registro de alumnos para un curso/capacitación, desarrollado para **Pi
Consulting**. Permite dar de alta, listar, buscar, editar y dar de baja alumnos (apellido,
nombre, DNI, fecha de nacimiento, teléfono y email opcionales).

## Estructura del repositorio

```
.
├── backend/         API REST — FastAPI + Clean Architecture (Python 3.12)
├── frontend/        Panel de gestión — React 19 + TypeScript (Vite)
├── data/            Datos persistidos localmente (SQLite). No se versiona el contenido.
├── postman/         Colección y environment de Postman para probar la API
├── branding-pi/     Brandbook y assets de identidad visual de Pi Consulting
├── TASKS.md         Tareas activas, pendientes y backlog
├── PROGRESS.md      Estado de avance por iteración y decisiones de diseño
└── CLAUDE.md        Convenciones de desarrollo del proyecto
```

Cada carpeta de código (`backend/`, `frontend/`) tiene su propio `README.md` con el detalle
de arquitectura, configuración y comandos.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | FastAPI, Pydantic v2, SQLAlchemy 2.0 (async), SQLite (`aiosqlite`) |
| Frontend | React 19, TypeScript, Vite, TanStack Query, React Hook Form + Zod |
| Base de datos | SQLite, archivo en `data/db/students.db` |
| Tests | pytest (backend) · Vitest + Testing Library (frontend) |
| Lint / Types | ruff + mypy --strict (backend) · oxlint + tsc (frontend) |

## Quickstart

Requisitos: Python 3.12 (vía `pyenv`, ver `.python-version`) y Node.js 20+.

**1. Backend** (`http://localhost:8000`)

```bash
cd backend
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

Swagger UI: http://localhost:8000/docs · Health check: `GET /health`

**2. Frontend** (`http://localhost:5173`)

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

El frontend consume el backend vía `VITE_API_BASE_URL` (`frontend/.env`) y el backend
tiene `http://localhost:5173` habilitado en CORS por defecto — no hace falta configuración
extra para levantar ambos en local.

Detalle completo de cada uno en [`backend/README.md`](backend/README.md) y
[`frontend/README.md`](frontend/README.md).

## Identidad visual

La UI del frontend sigue la identidad de marca definida en
[`branding-pi/Brandbook/Brandbook PI.pdf`](branding-pi/Brandbook/Brandbook%20PI.pdf):
Negro Pi (`#101212`) y Amarillo Pi (`#FFF100`) como colores primarios, paleta secundaria
para acentos, y tipografía Mona Sans. Ver el detalle de tokens en
[`frontend/README.md`](frontend/README.md#identidad-visual).

## Estado del proyecto

Ver [`TASKS.md`](TASKS.md) para el backlog y [`PROGRESS.md`](PROGRESS.md) para el historial
de decisiones de diseño por iteración.
