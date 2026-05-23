from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Nodo
from app.schemas.maestros import NodoCreate, NodoUpdate, NodoOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/nodos", tags=["nodos"])


@router.get("/", response_model=List[NodoOut])
async def list_nodos(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    sitio_id: Optional[str] = None,
    sector_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Nodo)
    if activo is not None:
        q = q.where(Nodo.activo == activo)
    if search:
        q = q.where(
            (Nodo.nombre.ilike(f"%{search}%"))
            | (Nodo.codigo.ilike(f"%{search}%"))
        )
    if sitio_id:
        q = q.where(Nodo.sitio_id == sitio_id)
    if sector_id:
        q = q.where(Nodo.sector_id == sector_id)
    q = q.order_by(Nodo.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{nodo_id}", response_model=NodoOut)
async def get_nodo(
    nodo_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Nodo).where(Nodo.id == nodo_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Nodo not found")
    return obj


@router.post("/", response_model=NodoOut, status_code=status.HTTP_201_CREATED)
async def create_nodo(
    data: NodoCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("NOD", db, Nodo)
    obj = Nodo(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="nodos", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Nodo creado: {obj.nombre} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{nodo_id}", response_model=NodoOut)
async def update_nodo(
    nodo_id: str,
    data: NodoUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Nodo).where(Nodo.id == nodo_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Nodo not found")
    for field, new_val in data.model_dump(exclude_unset=True).items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="nodos", registro_id=nodo_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{nodo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_nodo(
    nodo_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Nodo).where(Nodo.id == nodo_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Nodo not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="nodos", registro_id=nodo_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
