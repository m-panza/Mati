from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Vehiculo
from app.schemas.maestros import VehiculoCreate, VehiculoUpdate, VehiculoOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/vehiculos", tags=["vehiculos"])


@router.get("/", response_model=List[VehiculoOut])
async def list_vehiculos(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Vehiculo)
    if activo is not None:
        q = q.where(Vehiculo.activo == activo)
    if search:
        q = q.where(
            (Vehiculo.patente.ilike(f"%{search}%"))
            | (Vehiculo.codigo.ilike(f"%{search}%"))
            | (Vehiculo.tipo.ilike(f"%{search}%"))
        )
    q = q.order_by(Vehiculo.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{vehiculo_id}", response_model=VehiculoOut)
async def get_vehiculo(
    vehiculo_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Vehiculo).where(Vehiculo.id == vehiculo_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    return obj


@router.post("/", response_model=VehiculoOut, status_code=status.HTTP_201_CREATED)
async def create_vehiculo(
    data: VehiculoCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("VEH", db, Vehiculo)
    obj = Vehiculo(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="vehiculos", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Vehiculo creado: {obj.patente} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{vehiculo_id}", response_model=VehiculoOut)
async def update_vehiculo(
    vehiculo_id: str,
    data: VehiculoUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Vehiculo).where(Vehiculo.id == vehiculo_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    for field, new_val in data.model_dump(exclude_unset=True).items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="vehiculos", registro_id=vehiculo_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{vehiculo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_vehiculo(
    vehiculo_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Vehiculo).where(Vehiculo.id == vehiculo_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Vehiculo not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="vehiculos", registro_id=vehiculo_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
