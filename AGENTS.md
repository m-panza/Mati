# SIGRAV — Agent & Developer Guide

## Architecture

- **Backend**: FastAPI (Python 3.12), async SQLAlchemy, PostgreSQL 15, Alembic migrations
- **Frontend**: React 18, Vite 5, React Router v6, Leaflet maps
- **Infra**: Docker Compose, Nginx reverse proxy

## Commands

### Start everything
```bash
cp .env.example .env
docker compose up --build
```

### Apply migrations manually
```bash
docker compose exec backend alembic upgrade head
```

### Create a new migration
```bash
docker compose exec backend alembic revision --autogenerate -m "description"
```

### Run backend locally (no Docker)
```bash
cd backend
pip install -r requirements.txt
DATABASE_URL=postgresql+asyncpg://sigrav:sigrav123@localhost:5432/sigrav alembic upgrade head
uvicorn app.main:app --reload
```

### Run frontend locally (no Docker)
```bash
cd frontend
npm install
VITE_API_URL=http://localhost:8000 npm run dev
```

### View logs
```bash
docker compose logs -f backend
docker compose logs -f frontend
```

### Reset database
```bash
docker compose down -v  # removes pgdata volume
docker compose up --build
```

## Domain Rules

1. **No physical deletes** — All `DELETE` endpoints set `activo = False`. Never `db.delete(obj)`.

2. **Audit everything** — Every CREATE, UPDATE (per-field), and DEACTIVATE must write to the `auditoria` table via `app.utils.log_auditoria()`.

3. **Auto-generate codes** — Use `generate_codigo(prefix, db, Model)` on create. Never let the client supply a code.

4. **Tacho corriente change rule** — If a PUT to `/tachos/{id}` changes the `corriente_id`:
   - Deactivate the old tacho (set `activo=False`)
   - Create a new tacho with `version = old.version + 1`
   - Set `old.reemplazado_por_id = new.id`
   - Log audit for both records

5. **QR code resolution** — `GET /q/{codigo}` resolves the entity. The full URL is `{QR_BASE_URL}/{codigo}`.

## Data Model Summary

| Table | Codigo Prefix | Key Fields |
|-------|--------------|------------|
| users | — | email, rol (admin/supervisor/operador/visualizador) |
| sitios | SIT | nombre, latitud, longitud |
| sectores | SEC | sitio_id FK |
| corrientes | COR | color (hex) |
| clasificaciones | CLA | corriente_id FK |
| islas | ISL | sitio_id FK, sector_id FK nullable |
| tachos | TAC | isla_id FK, corriente_id FK, version int |
| nodos | NOD | sitio_id FK, sector_id FK nullable |
| islas_nodos | — | isla_id FK, nodo_id FK (M2M) |
| nodos_corrientes | — | nodo_id FK, corriente_id FK (M2M) |
| vehiculos | VEH | patente, capacidad_kg |
| receptores | REC | tipo enum, cuit |
| receptores_corrientes | — | receptor_id FK, corriente_id FK (M2M) |
| personas | PER | documento_tipo, documento_nro |
| personas_asignaciones | — | persona_id FK, entidad_tipo enum, entidad_id |
| qrcodes | — | codigo_qr unique, url_qr |
| documentos | — | entidad_tipo, entidad_id, ruta_archivo |
| auditoria | — | tabla, registro_id, accion, campo, valor_anterior, valor_nuevo |

## Roadmap Phases

1. **Phase 1 (Done)**: Core master data — Sitios, Sectores, Corrientes, Islas, Tachos, Nodos, Vehículos, Receptores, Personas
2. **Phase 2**: Retiros (waste pickups) — link Tachos/Nodos → Vehículo → Receptor, with peso_kg, foto
3. **Phase 3**: Pesajes (weigh events) — tare/gross weight capture per corriente
4. **Phase 4**: Reportes (reports) — aggregated CSV/Excel per site, stream, date range
5. **Phase 5**: Telegram bot integration — QR scan → bot message with entity info
6. **Phase 6**: Mobile PWA — offline-first for field operators
7. **Phase 7**: Advanced analytics — charts, trends, KPIs per site
8. **Phase 8**: Multi-tenant — multiple organizations per installation

## Coding Conventions

### Python
- Use `async def` for all route handlers and DB operations
- SQLAlchemy 2.x: `select(Model)`, `result.scalars().all()`
- Pydantic v2: `model_dump(exclude_unset=True)` (not `.dict()`)
- Import models lazily inside functions to avoid circular imports where needed
- All timestamps: `datetime.now(timezone.utc)` (timezone-aware)

### JavaScript / React
- Functional components with hooks only
- Inline styles using CSS custom properties (`var(--accent)`)
- `api` object from `src/api/client.js` for all requests
- Use `authFetch` for authenticated requests
- No TypeScript (plain JS with JSX)

## Testing Instructions

### Backend (manual)
1. Start with `docker compose up --build`
2. Visit http://localhost:8000/docs for interactive API docs
3. Login: POST `/auth/login` with `{"email":"admin@sigrav.local","password":"admin123"}`
4. Use Bearer token in Authorize button
5. Test CRUD on each entity

### Frontend (manual)
1. Visit http://localhost:5173
2. Login with admin@sigrav.local / admin123
3. Create a Sitio, then a Corriente, then an Isla (needs Sitio), then a Tacho (needs Isla + Corriente)
4. Generate a QR code for the Tacho
5. Check Auditoría for logged actions

### Database (direct)
```bash
docker compose exec db psql -U sigrav -d sigrav
\dt  -- list all tables
SELECT * FROM auditoria ORDER BY timestamp DESC LIMIT 10;
```
