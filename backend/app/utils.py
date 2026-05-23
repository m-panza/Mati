"""Shared utility functions for SIGRAV backend."""
from typing import Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def generate_codigo(prefix: str, db: AsyncSession, model) -> str:
    """
    Generate the next sequential code for a model.
    Example: prefix='SIT', returns 'SIT-000001', 'SIT-000002', etc.
    """
    # Query max existing code with this prefix
    result = await db.execute(
        select(func.max(model.codigo)).where(
            model.codigo.like(f"{prefix}-%")
        )
    )
    max_code = result.scalar()
    if max_code is None:
        next_num = 1
    else:
        # Extract the numeric part after the dash
        try:
            next_num = int(max_code.split("-", 1)[1]) + 1
        except (IndexError, ValueError):
            next_num = 1
    return f"{prefix}-{next_num:06d}"


async def log_auditoria(
    db: AsyncSession,
    tabla: str,
    registro_id: str,
    accion: str,
    usuario_id: Optional[str],
    usuario_email: str,
    campo: Optional[str] = None,
    valor_anterior: Optional[str] = None,
    valor_nuevo: Optional[str] = None,
    ip: Optional[str] = None,
    descripcion: Optional[str] = None,
):
    """Write an audit log entry."""
    from app.models.maestros import Auditoria

    entry = Auditoria(
        tabla=tabla,
        registro_id=registro_id,
        accion=accion,
        campo=campo,
        valor_anterior=valor_anterior,
        valor_nuevo=valor_nuevo,
        usuario_id=usuario_id,
        usuario_email=usuario_email,
        ip=ip,
        descripcion=descripcion,
    )
    db.add(entry)
    # Note: caller is responsible for commit
