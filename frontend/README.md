# Get Talent — Frontend

Panel de gestión de alumnos para el registro de un curso/capacitación. Construido con
React + TypeScript, consumiendo la API de `../backend`.

## Stack

| Capa | Tecnología |
|---|---|
| Build tool | Vite |
| UI | React 19 + TypeScript |
| Ruteo | React Router |
| Estado de servidor | TanStack Query |
| Formularios | React Hook Form + Zod |
| Cliente HTTP | Axios |
| Estilos | CSS Modules + design tokens de marca |
| Tipografía | Mona Sans (`@fontsource/mona-sans`) |
| Tests | Vitest + Testing Library |
| Lint | oxlint |

## Arquitectura

Organización por *feature* en lugar de por tipo de archivo, para que cada dominio
(sólo `students` por ahora) sea autocontenido y fácil de extender:

```
src/
  api/                Cliente HTTP y llamadas a la API (mapeo snake_case <-> camelCase)
  components/
    ui/                Primitivas reutilizables (Button, Field, Modal, Toast, ...)
    layout/            Layout de la aplicación (header de marca)
  features/
    students/
      components/      Formulario, tabla, paginación
      hooks/            Hooks de TanStack Query (list/create/update/delete)
      schemas/          Validación con Zod
      pages/            Página compuesta (StudentsPage)
  lib/                 Utilidades (formato, query client)
  styles/              Tokens de diseño + estilos globales
  types/               Tipos de dominio compartidos
```

Reglas seguidas:
- Los componentes de página consumen hooks de `features/*/hooks`, nunca llaman a `api/`
  directamente.
- El mapeo snake_case (backend) ↔ camelCase (frontend) vive únicamente en `api/students.ts`.
- Validación de formularios espejada 1:1 con las reglas del backend (DNI 7-8 dígitos,
  formato de email) para dar feedback inmediato sin esperar al submit.
- Componentes tipados con TypeScript estricto, sin `any`.

## Identidad visual

Tokens extraídos de `../branding-pi/Brandbook/Brandbook PI.pdf` en `src/styles/tokens.css`:

- Negro Pi `#101212` y Amarillo Pi `#FFF100` como colores primarios.
- Paleta secundaria (Cherry Pink, Naranja, Celeste, Azul Tech, Violeta) para estados y acentos.
- Tipografía **Mona Sans**, una de las dos fuentes oficiales de marca, vía `@fontsource`
  (open source, sin restricciones de licencia). La otra fuente de marca, **Nohemi**, es
  comercial y no está incluida en el repositorio — si se consigue la licencia, agregar los
  archivos de fuente y actualizar `--font-heading` en `src/styles/tokens.css`.

## Configuración

```bash
cp .env.example .env
```

| Variable | Descripción | Default |
|---|---|---|
| `VITE_API_BASE_URL` | URL base de la API del backend | `http://localhost:8000` |

## Desarrollo

```bash
npm install
npm run dev       # http://localhost:5173
```

El backend (`../backend`) debe estar corriendo en `http://localhost:8000` y tener
`http://localhost:5173` habilitado en `cors_allowed_origins` (ya configurado por defecto).

## Content Security Policy (dominios permitidos)

El build de producción (`npm run build`) inyecta automáticamente un
`<meta http-equiv="Content-Security-Policy">` en `index.html` (ver `csp.ts` y
`vite.config.ts`). Por defecto solo permite el propio origen (`'self'`) para scripts,
estilos, fuentes e imágenes; el **dominio permitido para llamadas de red** (`connect-src`)
se calcula automáticamente a partir de `VITE_API_BASE_URL` en build time — es decir, para
agregar o cambiar el dominio permitido no se toca la CSP a mano, se define la variable de
entorno:

```bash
# .env.production (no versionado) o variable de entorno en el pipeline de CI/CD
VITE_API_BASE_URL=https://api.get-talent.tu-dominio.com
```

Si `VITE_API_BASE_URL` no está definida al hacer build, `connect-src` queda limitado a
`'self'` (el frontend no podrá llamar a ningún backend externo) — es una medida
intencional para no terminar con una CSP permisiva por accidente.

Notas:
- El plugin (`csp.ts`, `apply: 'build'`) **no corre en `npm run dev`**: el dev server de
  Vite inyecta scripts inline para HMR que una CSP estricta bloquearía.
- Una `<meta>` CSP no soporta las directivas `frame-ancestors` ni `report-to`. Para un
  despliegue real (detrás de nginx, un CDN, etc.) es preferible además setear el header
  HTTP `Content-Security-Policy` a nivel del servidor/reverse proxy, por ejemplo:

  ```nginx
  add_header Content-Security-Policy "default-src 'self'; connect-src 'self' https://api.get-talent.tu-dominio.com; frame-ancestors 'none'" always;
  ```

## Scripts

| Comando | Descripción |
|---|---|
| `npm run dev` | Servidor de desarrollo |
| `npm run build` | Type-check + build de producción |
| `npm run preview` | Sirve el build de producción localmente |
| `npm run lint` | Lint con oxlint |
| `npm run test` | Corre la suite de tests una vez |
| `npm run test:watch` | Tests en modo watch |
| `npm run format` | Formatea el código con Prettier |

## Funcionalidad

- Listado paginado de alumnos.
- Alta de alumno (modal + validación).
- Edición parcial de alumno.
- Baja de alumno (con confirmación).
- Búsqueda por DNI.
- Feedback de errores de red/validación vía toasts, mapeando los códigos de error del
  backend (`404`, `409`, `422`).
