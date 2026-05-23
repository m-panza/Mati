import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.database import get_db
from app.dependencies import get_current_user
from app.models.maestros import (
    Sitio, Sector, Isla, Tacho, Nodo, Persona, Vehiculo, Receptor, Auditoria
)

router = APIRouter(prefix="/exportar", tags=["exportacion"])


def make_csv_response(rows: list, headers: list, filename: str) -> StreamingResponse:
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/sitios")
async def export_sitios(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sitio).order_by(Sitio.codigo))
    items = result.scalars().all()
    headers = ["codigo", "nombre", "alias", "descripcion", "direccion", "localidad",
               "provincia", "latitud", "longitud", "ubicacion_descriptiva", "activo",
               "created_at"]
    rows = [
        [s.codigo, s.nombre, s.alias, s.descripcion, s.direccion, s.localidad,
         s.provincia, s.latitud, s.longitud, s.ubicacion_descriptiva, s.activo,
         s.created_at.isoformat() if s.created_at else ""]
        for s in items
    ]
    return make_csv_response(rows, headers, "sitios.csv")


@router.get("/sectores")
async def export_sectores(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Sector).order_by(Sector.codigo))
    items = result.scalars().all()
    headers = ["codigo", "sitio_id", "nombre", "alias", "descripcion", "activo", "created_at"]
    rows = [
        [s.codigo, s.sitio_id, s.nombre, s.alias, s.descripcion, s.activo,
         s.created_at.isoformat() if s.created_at else ""]
        for s in items
    ]
    return make_csv_response(rows, headers, "sectores.csv")


@router.get("/islas")
async def export_islas(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Isla).order_by(Isla.codigo))
    items = result.scalars().all()
    headers = ["codigo", "sitio_id", "sector_id", "nombre", "alias", "descripcion",
               "latitud", "longitud", "ubicacion_descriptiva", "activo", "created_at"]
    rows = [
        [i.codigo, i.sitio_id, i.sector_id, i.nombre, i.alias, i.descripcion,
         i.latitud, i.longitud, i.ubicacion_descriptiva, i.activo,
         i.created_at.isoformat() if i.created_at else ""]
        for i in items
    ]
    return make_csv_response(rows, headers, "islas.csv")


@router.get("/tachos")
async def export_tachos(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Tacho).order_by(Tacho.codigo))
    items = result.scalars().all()
    headers = ["codigo", "isla_id", "corriente_id", "nombre", "alias", "color",
               "capacidad", "unidad_capacidad", "version", "activo", "created_at"]
    rows = [
        [t.codigo, t.isla_id, t.corriente_id, t.nombre, t.alias, t.color,
         t.capacidad, t.unidad_capacidad, t.version, t.activo,
         t.created_at.isoformat() if t.created_at else ""]
        for t in items
    ]
    return make_csv_response(rows, headers, "tachos.csv")


@router.get("/nodos")
async def export_nodos(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Nodo).order_by(Nodo.codigo))
    items = result.scalars().all()
    headers = ["codigo", "sitio_id", "sector_id", "nombre", "alias", "descripcion",
               "latitud", "longitud", "ubicacion_descriptiva", "activo", "created_at"]
    rows = [
        [n.codigo, n.sitio_id, n.sector_id, n.nombre, n.alias, n.descripcion,
         n.latitud, n.longitud, n.ubicacion_descriptiva, n.activo,
         n.created_at.isoformat() if n.created_at else ""]
        for n in items
    ]
    return make_csv_response(rows, headers, "nodos.csv")


@router.get("/personas")
async def export_personas(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Persona).order_by(Persona.codigo))
    items = result.scalars().all()
    headers = ["codigo", "nombre", "apellido", "email", "telefono",
               "documento_tipo", "documento_nro", "activo", "created_at"]
    rows = [
        [p.codigo, p.nombre, p.apellido, p.email, p.telefono,
         p.documento_tipo, p.documento_nro, p.activo,
         p.created_at.isoformat() if p.created_at else ""]
        for p in items
    ]
    return make_csv_response(rows, headers, "personas.csv")


@router.get("/vehiculos")
async def export_vehiculos(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Vehiculo).order_by(Vehiculo.codigo))
    items = result.scalars().all()
    headers = ["codigo", "patente", "tipo", "descripcion", "capacidad_kg",
               "activo", "created_at"]
    rows = [
        [v.codigo, v.patente, v.tipo, v.descripcion, v.capacidad_kg,
         v.activo, v.created_at.isoformat() if v.created_at else ""]
        for v in items
    ]
    return make_csv_response(rows, headers, "vehiculos.csv")


@router.get("/receptores")
async def export_receptores(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Receptor).order_by(Receptor.codigo))
    items = result.scalars().all()
    headers = ["codigo", "nombre", "tipo", "email", "telefono", "direccion",
               "cuit", "contacto_nombre", "es_provisorio", "activo", "created_at"]
    rows = [
        [r.codigo, r.nombre, r.tipo, r.email, r.telefono, r.direccion,
         r.cuit, r.contacto_nombre, r.es_provisorio, r.activo,
         r.created_at.isoformat() if r.created_at else ""]
        for r in items
    ]
    return make_csv_response(rows, headers, "receptores.csv")


@router.get("/auditoria")
async def export_auditoria(
    tabla: Optional[str] = None,
    accion: Optional[str] = None,
    fecha_desde: Optional[str] = Query(None, description="ISO date string"),
    fecha_hasta: Optional[str] = Query(None, description="ISO date string"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = select(Auditoria)
    if tabla:
        q = q.where(Auditoria.tabla == tabla)
    if accion:
        q = q.where(Auditoria.accion == accion)
    if fecha_desde:
        q = q.where(Auditoria.timestamp >= datetime.fromisoformat(fecha_desde))
    if fecha_hasta:
        q = q.where(Auditoria.timestamp <= datetime.fromisoformat(fecha_hasta))
    q = q.order_by(Auditoria.timestamp.desc())
    result = await db.execute(q)
    items = result.scalars().all()

    headers = ["id", "tabla", "registro_id", "accion", "campo", "valor_anterior",
               "valor_nuevo", "usuario_email", "ip", "timestamp", "descripcion"]
    rows = [
        [a.id, a.tabla, a.registro_id, a.accion, a.campo, a.valor_anterior,
         a.valor_nuevo, a.usuario_email, a.ip,
         a.timestamp.isoformat() if a.timestamp else "", a.descripcion]
        for a in items
    ]
    return make_csv_response(rows, headers, "auditoria.csv")
