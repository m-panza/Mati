from pydantic import BaseModel
from typing import Optional, List, TypeVar, Generic
from datetime import datetime

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int


class AuditoriaOut(BaseModel):
    id: str
    tabla: str
    registro_id: str
    accion: str
    campo: Optional[str] = None
    valor_anterior: Optional[str] = None
    valor_nuevo: Optional[str] = None
    usuario_id: Optional[str] = None
    usuario_email: str
    ip: Optional[str] = None
    timestamp: datetime
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
