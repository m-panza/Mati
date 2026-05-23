from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Persona
from app.schemas.maestros import PersonaCreate, PersonaUpdate, PersonaOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/personas", tags=["personas"])


@router.get("/", response_model=List[PersonaOut])
async def list_personas(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Persona)
    if activo is not None:
        q = q.where(Persona.activo == activo)
    if search:
        q = q.where(
            (Persona.nombre.ilike(f"%{search}%"))
            | (Persona.apellido.ilike(f"%{search}%"))
            | (Persona.codigo.ilike(f"%{search}%"))
            | (Persona.documento_nro.ilike(f"%{search}%"))
        )
    q = q.order_by(Persona.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{persona_id}", response_model=PersonaOut)
async def get_persona(
    persona_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Persona).where(Persona.id == persona_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Persona not found")
    return obj


@router.post("/", response_model=PersonaOut, status_code=status.HTTP_201_CREATED)
async def create_persona(
    data: PersonaCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("PER", db, Persona)
    obj = Persona(**data.model_dump(), codigo=codigo, created_by=current_user.id)
    db.add(obj)
    await db.flush()
    await log_auditoria(
        db=db, tabla="personas", registro_id=obj.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Persona creada: {obj.nombre} {obj.apellido} ({obj.codigo})",
    )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.put("/{persona_id}", response_model=PersonaOut)
async def update_persona(
    persona_id: str,
    data: PersonaUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Persona).where(Persona.id == persona_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Persona not found")
    for field, new_val in data.model_dump(exclude_unset=True).items():
        old_val = str(getattr(obj, field, None))
        setattr(obj, field, new_val)
        await log_auditoria(
            db=db, tabla="personas", registro_id=persona_id, accion="UPDATE",
            campo=field, valor_anterior=old_val, valor_nuevo=str(new_val),
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )
    await db.commit()
    await db.refresh(obj)
    return obj


@router.delete("/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_persona(
    persona_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Persona).where(Persona.id == persona_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Persona not found")
    obj.activo = False
    await log_auditoria(
        db=db, tabla="personas", registro_id=persona_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
