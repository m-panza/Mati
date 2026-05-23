# SIGRAV — Sistema Integral de Gestión de Residuos y Activos Valorizables

SIGRAV is a comprehensive web application for managing waste streams, collection sites, bins, transport vehicles, and receiving organizations. It provides full traceability with QR codes, audit logging, and geolocation features.

## Stack

- **Backend**: FastAPI + SQLAlchemy (async) + PostgreSQL + Alembic
- **Frontend**: React 18 + Vite + React Router + Leaflet maps
- **Infrastructure**: Docker Compose + Nginx

## Quick Start

```bash
cp .env.example .env
docker compose up --build
```

### Access URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| API (FastAPI docs) | http://localhost:8000/docs |
| PostgreSQL | localhost:5432 |

### Default Credentials

- **Email**: admin@sigrav.local
- **Password**: admin123

> Change this password immediately in production.

## Module Overview

### Sitios & Sectores
Sites are physical locations (buildings, campuses) organized into optional sectors. Each site can have GPS coordinates displayed on the built-in map.

### Corrientes & Clasificaciones
Waste streams define the categories of waste (e.g., organic, plastic, glass). Each stream can have sub-classifications for more granular tracking. Streams are color-coded for visual identification.

### Islas & Tachos
Waste islands are groupings of bins within a site/sector. Each bin (tacho) belongs to an island and is assigned to a waste stream. When a bin's stream changes, a new versioned record is created and the old one is deactivated — preserving full history.

### Nodos
Accumulation nodes are intermediate collection points where waste from multiple islands is consolidated before transport. They support many-to-many links with islands and streams.

### Vehículos & Receptores
Vehicles track the fleet used for collection. Receivers (cooperativas, foundations, operators) are the end destinations for collected waste.

### Personas & Asignaciones
People can be assigned to sites, islands, or nodes with specific roles (responsable, suplente, operador).

### QR Codes
Every tacho, isla, and nodo can have a QR code generated. Scanning resolves to a configurable URL (e.g., Telegram bot integration at `QR_BASE_URL`).

### Auditoría
Every CREATE, UPDATE, and DEACTIVATE action is logged with the old/new values, timestamp, user, and IP address.

## Development Setup

### Backend (without Docker)

```bash
cd backend
pip install -r requirements.txt
# Start a local Postgres, then:
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend (without Docker)

```bash
cd frontend
npm install
npm run dev
```

Set `VITE_API_URL=http://localhost:8000` in `frontend/.env.local` if running backend directly.
