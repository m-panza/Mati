from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Corriente, Clasificacion
from app.schemas.maestros import (
    CorrienteCreate, CorrienteUpdate, CorrienteOut,
    ClasificacionCreate, ClasificacionUpdate, ClasificacionOut,
)
from app.utils import generate_codigo, log_auditoria

router = APIRouter(tags=["corrientes"])


# ─── Corrientes ───────────────────────────────────────────────────────────────

@router.get("/corrientes", response_model=List[CorrienteOut])
async def list_corrientes(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Corriente)
    if activo is not None:
        q = q.where(Corriente.activo == activo)
    if search:
        q = q.where(
            (Corriente.nombre.ilike(f"%{search}%"))
            | (Corriente.codigo.ilike(f"%{search}%"))
        )
    q = q.order_by(Corriente.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/corrientes/{corriente_id}", response_model=CorrienteOut)
async def get_corriente(
    corriente_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Corriente).where(Corriente.id == corriente_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Corriente not found")
    return obj


@router.post("/corrientes", response_model=CorrienteOut, status_code=status.HTTP_201_CREATED)
async def create_corriente(
    data: CorrienteCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("COR", db, Corriente)
    obj = Corriente(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="corrientes", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Corriente creada: {obj.nombre} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/corrientes/{corriente_id}", response_model=CorrienteOut)
async def update_corriente(
    corriente_id: str,
    data: CorrienteUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Corriente).where(Corriente.id == corriente_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Corriente not found")
    for field, new_val in data.model_dump(exclude_unset=True).items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="corrientes", registro_id=corriente_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/corrientes/{corriente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_corriente(
    corriente_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Corriente).where(Corriente.id == corriente_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Corriente not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="corrientes", registro_id=corriente_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()


# ─── Clasificaciones ──────────────────────────────────────────────────────────

@router.get("/clasificaciones", response_model=List[ClasificacionOut])
async def list_clasificaciones(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    corriente_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Clasificacion)
    if activo is not None:
        q = q.where(Clasificacion.activo == activo)
    if search:
        q = q.where(Clasificacion.nombre.ilike(f"%{search}%"))
    if corriente_id:
        q = q.where(Clasificacion.corriente_id == corriente_id)
    q = q.order_by(Clasificacion.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/clasificaciones/{clas_id}", response_model=ClasificacionOut)
async def get_clasificacion(
    clas_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Clasificacion).where(Clasificacion.id == clas_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Clasificacion not found")
    return obj


@router.post("/clasificaciones", response_model=ClasificacionOut, status_code=status.HTTP_201_CREATED)
async def create_clasificacion(
    data: ClasificacionCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("CLA", db, Clasificacion)
    obj = Clasificacion(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="clasificaciones", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Clasificacion creada: {obj.nombre} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/clasificaciones/{clas_id}", response_model=ClasificacionOut)
async def update_clasificacion(
    clas_id: str,
    data: ClasificacionUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Clasificacion).where(Clasificacion.id == clas_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Clasificacion not found")
    for field, new_val in data.model_dump(exclude_unset=True).items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="clasificaciones", registro_id=clas_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/clasificaciones/{clas_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_clasificacion(
    clas_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Clasificacion).where(Clasificacion.id == clas_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Clasificacion not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="clasificaciones", registro_id=clas_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
