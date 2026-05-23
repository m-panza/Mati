from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import uuid

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Tacho
from app.schemas.maestros import TachoCreate, TachoUpdate, TachoOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/tachos", tags=["tachos"])


@router.get("/", response_model=List[TachoOut])
async def list_tachos(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    isla_id: Optional[str] = None,
    corriente_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Tacho)
    if activo is not None:
        q = q.where(Tacho.activo == activo)
    if search:
        q = q.where(
            (Tacho.nombre.ilike(f"%{search}%"))
            | (Tacho.codigo.ilike(f"%{search}%"))
        )
    if isla_id:
        q = q.where(Tacho.isla_id == isla_id)
    if corriente_id:
        q = q.where(Tacho.corriente_id == corriente_id)
    q = q.order_by(Tacho.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{tacho_id}", response_model=TachoOut)
async def get_tacho(
    tacho_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Tacho).where(Tacho.id == tacho_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Tacho not found")
    return obj


@router.post("/", response_model=TachoOut, status_code=status.HTTP_201_CREATED)
async def create_tacho(
    data: TachoCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("TAC", db, Tacho)
    obj = Tacho(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="tachos", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Tacho creado: {obj.nombre} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{tacho_id}", response_model=TachoOut)
async def update_tacho(
    tacho_id: str,
    data: TachoUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Tacho).where(Tacho.id == tacho_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Tacho not found")

    update_data = data.model_dump(exclude_unset=True)

    # Special rule: if corriente changes, deactivate old and create new version
    if "corriente_id" in update_data and update_data["corriente_id"] != obj.corriente_id:
        old_corriente = obj.corriente_id
        # Deactivate old tacho
        obj.activo = False
        obj.reemplazado_por_id = None  # will be set after new tacho is created

        # Create new tacho with incremented version
        new_codigo = await generate_codigo("TAC", db, Tacho)
        new_tacho = Tacho(
            isla_id=update_data.get("isla_id", obj.isla_id),
            corriente_id=update_data["corriente_id"],
            nombre=update_data.get("nombre", obj.nombre),
            alias=update_data.get("alias", obj.alias),
            color=update_data.get("color", obj.color),
            capacidad=update_data.get("capacidad", obj.capacidad),
            unidad_capacidad=update_data.get("unidad_capacidad", obj.unidad_capacidad),
            version=obj.version + 1,
            codigo=new_codigo,
            created_by=current_user.id,
        )
        db.add(new_tacho)
        await db.flush()
        obj.reemplazado_por_id = new_tacho.id

        await log_auditoria(
            db=db, tabla="tachos", registro_id=tacho_id, accion="DEACTIVATE",
            campo="corriente_id", valor_anterior=old_corriente,
            valor_nuevo=update_data["corriente_id"],
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
            descripcion=f"Tacho reemplazado por corriente change: nuevo ID={new_tacho.id}",
        )
        await log_auditoria(
            db=db, tabla="tachos", registro_id=new_tacho.id, accion="CREATE",
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
            descripcion=f"Tacho nueva versión v{new_tacho.version} por cambio de corriente",
        )
        await db.commit()
        await db.refresh(new_tacho)
        return new_tacho

    # Normal update (no corriente change)
    for field, new_val in update_data.items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="tachos", registro_id=tacho_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{tacho_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_tacho(
    tacho_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Tacho).where(Tacho.id == tacho_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Tacho not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="tachos", registro_id=tacho_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
