from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Sitio
from app.schemas.maestros import SitioCreate, SitioUpdate, SitioOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/sitios", tags=["sitios"])


@router.get("/", response_model=List[SitioOut])
async def list_sitios(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Sitio)
    if activo is not None:
        q = q.where(Sitio.activo == activo)
    if search:
        q = q.where(
            (Sitio.nombre.ilike(f"%{search}%"))
            | (Sitio.codigo.ilike(f"%{search}%"))
            | (Sitio.alias.ilike(f"%{search}%"))
        )
    q = q.order_by(Sitio.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{sitio_id}", response_model=SitioOut)
async def get_sitio(
    sitio_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sitio).where(Sitio.id == sitio_id))
    sitio = result.scalar_one_or_none()
    if not sitio:
        raise HTTPException(status_code=404, detail="Sitio not found")
    return sitio


@router.post("/", response_model=SitioOut, status_code=status.HTTP_201_CREATED)
async def create_sitio(
    data: SitioCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("SIT", db, Sitio)
    sitio = Sitio(
        **data.model_dump(),
        codigo=codigo,
        created_by=current_user.id,
    )
    db.add(sitio)
    await db.flush()

    await log_auditoria(
        db=db,
        tabla="sitios",
        registro_id=sitio.id,
        accion="CREATE",
        usuario_id=current_user.id,
        usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Sitio creado: {sitio.nombre} ({sitio.codigo})",
    )

    await db.commit()
    await db.refresh(sitio)
    return sitio


@router.put("/{sitio_id}", response_model=SitioOut)
async def update_sitio(
    sitio_id: str,
    data: SitioUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sitio).where(Sitio.id == sitio_id))
    sitio = result.scalar_one_or_none()
    if not sitio:
        raise HTTPException(status_code=404, detail="Sitio not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, new_val in update_data.items():
        old_val = str(getattr(sitio, field, None))
        setattr(sitio, field, new_val)
        await log_auditoria(
            db=db,
            tabla="sitios",
            registro_id=sitio_id,
            accion="UPDATE",
            campo=field,
            valor_anterior=old_val,
            valor_nuevo=str(new_val),
            usuario_id=current_user.id,
            usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )

    await db.commit()
    await db.refresh(sitio)
    return sitio


@router.delete("/{sitio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_sitio(
    sitio_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sitio).where(Sitio.id == sitio_id))
    sitio = result.scalar_one_or_none()
    if not sitio:
        raise HTTPException(status_code=404, detail="Sitio not found")

    sitio.activo = False
    await log_auditoria(
        db=db,
        tabla="sitios",
        registro_id=sitio_id,
        accion="DEACTIVATE",
        usuario_id=current_user.id,
        usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
