# SIGRAV — Technical Context for AI Coding Assistants

## Architecture Overview

```
frontend (React/Vite) → /api/* → nginx → backend (FastAPI) → PostgreSQL
```

- Frontend served on port 5173 (dev) / 80 (production via nginx)
- Backend served on port 8000
- Nginx in the frontend container proxies `/api/` → `http://backend:8000/`
- All frontend API calls use `VITE_API_URL` env var (defaults to `/api`)

## Backend Structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app, startup seeder, router registration
│   ├── config.py        # pydantic-settings (reads .env)
│   ├── database.py      # async SQLAlchemy engine + Base
│   ├── dependencies.py  # get_db, get_current_user, require_admin, require_supervisor
│   ├── utils.py         # generate_codigo(), log_auditoria()
│   ├── auth/            # JWT login, /auth/login, /auth/me
│   ├── models/          # SQLAlchemy ORM models
│   │   ├── users.py     # User model
│   │   └── maestros.py  # ALL domain models
│   ├── schemas/         # Pydantic schemas
│   │   ├── common.py    # AuditoriaOut, PaginatedResponse
│   │   ├── users.py     # UserCreate/Update/Out
│   │   └── maestros.py  # All entity schemas
│   └── routers/         # One file per entity
└── alembic/             # DB migrations
```

## Database Schema Summary

All entity tables follow this pattern:
- `id` VARCHAR(36) UUID PK
- `codigo` VARCHAR(20) UNIQUE (auto-generated, e.g. `SIT-000001`)
- domain fields...
- `activo` BOOLEAN DEFAULT true
- `created_at`, `updated_at` TIMESTAMPTZ
- `created_by` FK → users.id

### Code Prefixes
| Entity | Prefix | Example |
|--------|--------|---------|
| Sitio | SIT | SIT-000001 |
| Sector | SEC | SEC-000001 |
| Corriente | COR | COR-000001 |
| Clasificacion | CLA | CLA-000001 |
| Isla | ISL | ISL-000001 |
| Tacho | TAC | TAC-000001 |
| Nodo | NOD | NOD-000001 |
| Vehiculo | VEH | VEH-000001 |
| Receptor | REC | REC-000001 |
| Persona | PER | PER-000001 |

### Key Relationships
- Sector → Sitio (FK)
- Isla → Sitio + optional Sector
- Tacho → Isla + Corriente (stream change = new version)
- Nodo → Sitio + optional Sector
- IslaNodo: many-to-many Isla ↔ Nodo
- NodoCorriente: many-to-many Nodo ↔ Corriente
- ReceptorCorriente: many-to-many Receptor ↔ Corriente
- PersonaAsignacion: Persona → (sitio|isla|nodo) with role

## API Conventions

### No Physical Deletes
All DELETE endpoints set `activo = False`. Physical records are never removed from the database.

### Audit Logging
Every mutating operation writes to the `auditoria` table:
```python
await log_auditoria(db, tabla, registro_id, accion, usuario_id, usuario_email, 
                    campo, valor_anterior, valor_nuevo, ip, descripcion)
```
- `accion`: `CREATE`, `UPDATE`, `DEACTIVATE`, `REACTIVATE`
- For UPDATE: one audit row per changed field

### Auto Code Generation
```python
codigo = await generate_codigo("SIT", db, Sitio)
# Returns "SIT-000001", increments max existing
```

### Default Filters
All list endpoints default to `activo=true`. Pass `activo=false` or no filter to get all records.

## Business Rules

1. **No physical deletes** — only `activo = False`
2. **Tacho corriente change** — creates new Tacho record (version+1), deactivates old one, sets `reemplazado_por_id`
3. **QR codes** — each entity (tacho/isla/nodo) gets one QR code (its `codigo`). URL: `{QR_BASE_URL}/{codigo}`
4. **Audit everything** — CREATE, UPDATE (field-by-field), DEACTIVATE all logged
5. **Auto-seeded admin** — if no users exist at startup, creates `admin@sigrav.local` / `admin123`

## Auth

- JWT Bearer tokens via `/auth/login`
- Token stored in `localStorage` as `sigrav_token`
- Roles: `admin` > `supervisor` > `operador` > `visualizador`
- `require_admin`: admin only
- `require_supervisor`: admin or supervisor
- `get_current_user`: any authenticated user

## Frontend Structure

```
src/
├── api/client.js      # authFetch + api object with all entity methods
├── auth/AuthContext.jsx
├── components/
│   ├── Layout.jsx     # Sidebar + Outlet
│   ├── Sidebar.jsx    # Nav with all entities
│   ├── CrudTable.jsx  # Generic CRUD table + modal form
│   ├── Modal.jsx
│   └── MapView.jsx    # Leaflet map
└── pages/             # One page per entity + Dashboard, QR, Auditoria
```

## Coding Conventions

- Python: async/await throughout, SQLAlchemy 2.x style (`select()`, `scalars()`)
- No `relationship()` defined — use explicit FK queries for simplicity
- Pydantic v2 (`model_dump(exclude_unset=True)` not `.dict()`)
- React: functional components, hooks, inline styles (no CSS framework)
- All entity list endpoints accept: `activo`, `search`, `skip`, `limit` query params
