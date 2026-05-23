from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Isla
from app.schemas.maestros import IslaCreate, IslaUpdate, IslaOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/islas", tags=["islas"])


@router.get("/", response_model=List[IslaOut])
async def list_islas(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    sitio_id: Optional[str] = None,
    sector_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Isla)
    if activo is not None:
        q = q.where(Isla.activo == activo)
    if search:
        q = q.where(
            (Isla.nombre.ilike(f"%{search}%"))
            | (Isla.codigo.ilike(f"%{search}%"))
        )
    if sitio_id:
        q = q.where(Isla.sitio_id == sitio_id)
    if sector_id:
        q = q.where(Isla.sector_id == sector_id)
    q = q.order_by(Isla.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{isla_id}", response_model=IslaOut)
async def get_isla(
    isla_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Isla).where(Isla.id == isla_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Isla not found")
    return obj


@router.post("/", response_model=IslaOut, status_code=status.HTTP_201_CREATED)
async def create_isla(
    data: IslaCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("ISL", db, Isla)
    obj = Isla(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="islas", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Isla creada: {obj.nombre} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{isla_id}", response_model=IslaOut)
async def update_isla(
    isla_id: str,
    data: IslaUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Isla).where(Isla.id == isla_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Isla not found")
    for field, new_val in data.model_dump(exclude_unset=True).items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="islas", registro_id=isla_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{isla_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_isla(
    isla_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Isla).where(Isla.id == isla_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Isla not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="islas", registro_id=isla_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
