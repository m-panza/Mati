import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import AsyncSessionLocal

logger = logging.getLogger(__name__)


async def seed_admin():
    """Create default admin user if no users exist."""
    from sqlalchemy import select, func
    from app.models.users import User
    from app.auth.utils import hash_password

    async with AsyncSessionLocal() as db:
        result = await db.execute(select(func.count()).select_from(User))
        count = result.scalar()
        if count == 0:
            admin = User(
                email="admin@sigrav.local",
                nombre="Admin",
                apellido="SIGRAV",
                password_hash=hash_password("admin123"),
                rol="admin",
                activo=True,
            )
            db.add(admin)
            await db.commit()
            logger.info("Created default admin user: admin@sigrav.local / admin123")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    os.makedirs(settings.uploads_dir, exist_ok=True)
    await seed_admin()
    yield
    # Shutdown


app = FastAPI(
    title="SIGRAV API",
    description="Sistema Integral de Gestión de Residuos y Activos Valorizables",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving files
os.makedirs(settings.uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.uploads_dir), name="uploads")

# Import and include routers
from app.auth.router import router as auth_router
from app.routers.users import router as users_router
from app.routers.sitios import router as sitios_router
from app.routers.sectores import router as sectores_router
from app.routers.islas import router as islas_router
from app.routers.tachos import router as tachos_router
from app.routers.nodos import router as nodos_router
from app.routers.corrientes import router as corrientes_router
from app.routers.vehiculos import router as vehiculos_router
from app.routers.receptores import router as receptores_router
from app.routers.personas import router as personas_router
from app.routers.qr import router as qr_router
from app.routers.documentos import router as documentos_router
from app.routers.exportacion import router as exportacion_router
from app.routers.auditoria import router as auditoria_router

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(sitios_router)
app.include_router(sectores_router)
app.include_router(islas_router)
app.include_router(tachos_router)
app.include_router(nodos_router)
app.include_router(corrientes_router)
app.include_router(vehiculos_router)
app.include_router(receptores_router)
app.include_router(personas_router)
app.include_router(qr_router)
app.include_router(documentos_router)
app.include_router(exportacion_router)
app.include_router(auditoria_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "SIGRAV API"}
