from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from datetime import datetime

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Auditoria
from app.schemas.common import AuditoriaOut

router = APIRouter(prefix="/auditoria", tags=["auditoria"])


@router.get("/", response_model=List[AuditoriaOut])
async def list_auditoria(
    tabla: Optional[str] = None,
    accion: Optional[str] = None,
    registro_id: Optional[str] = None,
    fecha_desde: Optional[str] = Query(None),
    fecha_hasta: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 500,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Auditoria)
    if tabla:
        q = q.where(Auditoria.tabla == tabla)
    if accion:
        q = q.where(Auditoria.accion == accion)
    if registro_id:
        q = q.where(Auditoria.registro_id == registro_id)
    if fecha_desde:
        q = q.where(Auditoria.timestamp >= datetime.fromisoformat(fecha_desde))
    if fecha_hasta:
        q = q.where(Auditoria.timestamp <= datetime.fromisoformat(fecha_hasta))
    q = q.order_by(Auditoria.timestamp.desc()).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()
