from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Sector
from app.schemas.maestros import SectorCreate, SectorUpdate, SectorOut
from app.utils import generate_codigo, log_auditoria

router = APIRouter(prefix="/sectores", tags=["sectores"])


@router.get("/", response_model=List[SectorOut])
async def list_sectores(
    activo: Optional[bool] = True,
    search: Optional[str] = None,
    sitio_id: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Sector)
    if activo is not None:
        q = q.where(Sector.activo == activo)
    if search:
        q = q.where(
            (Sector.nombre.ilike(f"%{search}%"))
            | (Sector.codigo.ilike(f"%{search}%"))
        )
    if sitio_id:
        q = q.where(Sector.sitio_id == sitio_id)
    q = q.order_by(Sector.codigo).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.get("/{sector_id}", response_model=SectorOut)
async def get_sector(
    sector_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sector).where(Sector.id == sector_id))
    sector = result.scalar_one_or_none()
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")
    return sector


@router.post("/", response_model=SectorOut, status_code=status.HTTP_201_CREATED)
async def create_sector(
    data: SectorCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    codigo = await generate_codigo("SEC", db, Sector)
    sector = Sector(
        **data.model_dump(),
        codigo=codigo,
        created_by=current_user.id,
    )
    db.add(sector)
    await db.flush()

    await log_auditoria(
        db=db,
        tabla="sectores",
        registro_id=sector.id,
        accion="CREATE",
        usuario_id=current_user.id,
        usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Sector creado: {sector.nombre} ({sector.codigo})",
    )

    await db.commit()
    await db.refresh(sector)
    return sector


@router.put("/{sector_id}", response_model=SectorOut)
async def update_sector(
    sector_id: str,
    data: SectorUpdate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sector).where(Sector.id == sector_id))
    sector = result.scalar_one_or_none()
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, new_val in update_data.items():
        old_val = str(getattr(sector, field, None))
        setattr(sector, field, new_val)
        await log_auditoria(
            db=db,
            tabla="sectores",
            registro_id=sector_id,
            accion="UPDATE",
            campo=field,
            valor_anterior=old_val,
            valor_nuevo=str(new_val),
            usuario_id=current_user.id,
            usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
        )

    await db.commit()
    await db.refresh(sector)
    return sector


@router.delete("/{sector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_sector(
    sector_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sector).where(Sector.id == sector_id))
    sector = result.scalar_one_or_none()
    if not sector:
        raise HTTPException(status_code=404, detail="Sector not found")

    sector.activo = False
    await log_auditoria(
        db=db,
        tabla="sectores",
        registro_id=sector_id,
        accion="DEACTIVATE",
        usuario_id=current_user.id,
        usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
