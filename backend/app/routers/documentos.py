import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, Request, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import Documento
from app.schemas.maestros import DocumentoOut
from app.config import settings
from app.utils import log_auditoria

router = APIRouter(prefix="/documentos", tags=["documentos"])


@router.post("/upload", response_model=DocumentoOut, status_code=status.HTTP_201_CREATED)
async def upload_documento(
    request: Request,
    entidad_tipo: str = Form(...),
    entidad_id: str = Form(...),
    descripcion: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Save file
    doc_dir = os.path.join(settings.uploads_dir, "documentos", entidad_tipo, entidad_id)
    os.makedirs(doc_dir, exist_ok=True)

    file_ext = os.path.splitext(file.filename)[1] if file.filename else ""
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = os.path.join(doc_dir, unique_filename)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Relative path for storage
    ruta_relativa = os.path.join("documentos", entidad_tipo, entidad_id, unique_filename)

    doc = Documento(
        entidad_tipo=entidad_tipo,
        entidad_id=entidad_id,
        nombre_archivo=file.filename or unique_filename,
        tipo_mime=file.content_type,
        ruta_archivo=ruta_relativa,
        descripcion=descripcion,
        uploaded_by=current_user.id,
    )
    db.add(doc)
    await db.flush()

    await log_auditoria(
        db=db, tabla="documentos", registro_id=doc.id, accion="CREATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
        descripcion=f"Documento subido: {file.filename} para {entidad_tipo}/{entidad_id}",
    )

    await db.commit()
    await db.refresh(doc)
    return doc


@router.get("/", response_model=List[DocumentoOut])
async def list_documentos(
    entidad_tipo: Optional[str] = None,
    entidad_id: Optional[str] = None,
    activo: Optional[bool] = True,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Documento)
    if activo is not None:
        q = q.where(Documento.activo == activo)
    if entidad_tipo:
        q = q.where(Documento.entidad_tipo == entidad_tipo)
    if entidad_id:
        q = q.where(Documento.entidad_id == entidad_id)
    q = q.order_by(Documento.uploaded_at.desc()).offset(skip).limit(limit)
    result = await db.execute(q)
    return result.scalars().all()


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deactivate_documento(
    doc_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Documento).where(Documento.id == doc_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento not found")
    doc.activo = False
    await log_auditoria(
        db=db, tabla="documentos", registro_id=doc_id, accion="DEACTIVATE",
        usuario_id=current_user.id, usuario_email=current_user.email,
        ip=request.client.host if request.client else None,
    )
    await db.commit()
