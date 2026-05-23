from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Receptor
from app.schemas.maestros import ReceptorCreate, ReceptorUpdate, ReceptorOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/receptores", tags=["receptores"])


@router.get("/", response_model=List[ReceptorOut])
async def list_receptores(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    tipo: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Receptor)
    if activo is not None:
        q = q.where(Receptor.activo == activo)
    if search:
        q = q.where(
            (Receptor.nombre.ilike(f"%{search}%"))
            | (Receptor.codigo.ilike(f"%{search}%"))
        )
    if tipo:
        q = q.where(Receptor.tipo == tipo)
    q = q.order_by(Receptor.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{receptor_id}", response_model=ReceptorOut)
async def get_receptor(
    receptor_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Receptor).where(Receptor.id == receptor_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Receptor not found")
    return obj


@router.post("/", response_model=ReceptorOut, status_code=status.HTTP_201_CREATED)
async def create_receptor(
    data: ReceptorCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("REC", db, Receptor)
    obj = Receptor(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="receptores", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Receptor creado: {obj.nombre} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{receptor_id}", response_model=ReceptorOut)
async def update_receptor(
    receptor_id: str,
    data: ReceptorUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Receptor).where(Receptor.id == receptor_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Receptor not found")
    for field, new_val in data.model_dump(exclude_unset=True).items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="receptores", registro_id=receptor_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{receptor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_receptor(
    receptor_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Receptor).where(Receptor.id == receptor_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Receptor not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="receptores", registro_id=receptor_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
