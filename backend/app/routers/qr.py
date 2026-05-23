import os
import io
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse, RedirectResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import QRCode, Tacho, Isla, Nodo
from app.schemas.maestros import QRGenerar, QRCodeOut
from app.config import settings
from app.utils import log_auditoria

router = APIRouter(tags=["qr"])


def _get_entity_codigo(entidad_tipo: str, entity) -> str:
    return entity.codigo


async def _get_entity(db: AsyncSession, entidad_tipo: str, entidad_id: str):
    model_map = {"tacho": Tacho, "isla": Isla, "nodo": Nodo}
    model = model_map.get(entidad_tipo)
    if not model:
        raise HTTPException(status_code=400, detail=f"Unknown entidad_tipo: {entidad_tipo}")
    result = await db.execute(select(model).where(model.id == entidad_id))
    entity = result.scalar_one_or_none()
    if not entity:
        raise HTTPException(status_code=404, detail=f"{entidad_tipo} not found")
    return entity


@router.post("/qr/generar", response_model=QRCodeOut)
async def generar_qr(
    data: QRGenerar,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    import qrcode
    from PIL import Image

    entity = await _get_entity(db, data.entidad_tipo, data.entidad_id)
    codigo_qr = entity.codigo
    url_qr = f"{settings.qr_base_url}/{codigo_qr}"

    # Check if QR already exists
    existing = await db.execute(
        select(QRCode).where(QRCode.codigo_qr == codigo_qr)
    )
    qr_record = existing.scalar_one_or_none()

    if not qr_record:
        # Generate QR image
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url_qr)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Save to uploads
        qr_dir = os.path.join(settings.uploads_dir, "qr")
        os.makedirs(qr_dir, exist_ok=True)
        img_path = os.path.join(qr_dir, f"{codigo_qr}.png")
        img.save(img_path)

        qr_record = QRCode(
            entidad_tipo=data.entidad_tipo,
            entidad_id=data.entidad_id,
            codigo_qr=codigo_qr,
            url_qr=url_qr,
            generado_por=current_user.id,
        )
        db.add(qr_record)
        await db.flush()
        await log_auditoria(
            db=db, tabla="qrcodes", registro_id=qr_record.id, accion="CREATE",
            usuario_id=current_user.id, usuario_email=current_user.email,
            ip=request.client.host if request.client else None,
            descripcion=f"QR generado para {data.entidad_tipo} {codigo_qr}",
        )
        await db.commit()
        await db.refresh(qr_record)

    return qr_record


@router.get("/qr/{entidad_tipo}/{entidad_id}", response_model=QRCodeOut)
async def get_qr_for_entity(
    entidad_tipo: str,
    entidad_id: str,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    entity = await _get_entity(db, entidad_tipo, entidad_id)
    result = await db.execute(
        select(QRCode).where(QRCode.entidad_id == entidad_id, QRCode.entidad_tipo == entidad_tipo)
    )
    qr_record = result.scalar_one_or_none()
    if not qr_record:
        raise HTTPException(status_code=404, detail="QR not generated yet")
    return qr_record


@router.get("/qr/imagen/{codigo_qr}")
async def get_qr_image(codigo_qr: str):
    img_path = os.path.join(settings.uploads_dir, "qr", f"{codigo_qr}.png")
    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="QR image not found")
    return FileResponse(img_path, media_type="image/png")


@router.get("/q/{codigo}")
async def qr_redirect(codigo: str, db: AsyncSession = Depends(get_db)):
    """Public redirect endpoint for QR codes."""
    result = await db.execute(select(QRCode).where(QRCode.codigo_qr == codigo))
    qr_record = result.scalar_one_or_none()
    if not qr_record:
        raise HTTPException(status_code=404, detail="QR code not found")
    # Return info for Telegram bot redirect
    return {
        "codigo": codigo,
        "entidad_tipo": qr_record.entidad_tipo,
        "entidad_id": qr_record.entidad_id,
        "url_qr": qr_record.url_qr,
    }
