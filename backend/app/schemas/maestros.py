from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ─── Persona ─────────────────────────────────────────────────────────────────

class PersonaCreate(BaseModel):
    nombre: str
    apellido: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    documento_tipo: Optional[str] = None
    documento_nro: Optional[str] = None


class PersonaUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    documento_tipo: Optional[str] = None
    documento_nro: Optional[str] = None
    activo: Optional[bool] = None


class PersonaOut(BaseModel):
    id: str
    codigo: str
    nombre: str
    apellido: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    documento_tipo: Optional[str] = None
    documento_nro: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Sitio ────────────────────────────────────────────────────────────────────

class SitioCreate(BaseModel):
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    direccion: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None


class SitioUpdate(BaseModel):
    nombre: Optional[str] = None
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    direccion: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None
    activo: Optional[bool] = None


class SitioOut(BaseModel):
    id: str
    codigo: str
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    direccion: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Sector ───────────────────────────────────────────────────────────────────

class SectorCreate(BaseModel):
    sitio_id: str
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None


class SectorUpdate(BaseModel):
    sitio_id: Optional[str] = None
    nombre: Optional[str] = None
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class SectorOut(BaseModel):
    id: str
    codigo: str
    sitio_id: str
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Corriente ────────────────────────────────────────────────────────────────

class CorrienteCreate(BaseModel):
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    color: Optional[str] = None


class CorrienteUpdate(BaseModel):
    nombre: Optional[str] = None
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    color: Optional[str] = None
    activo: Optional[bool] = None


class CorrienteOut(BaseModel):
    id: str
    codigo: str
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    color: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Clasificacion ────────────────────────────────────────────────────────────

class ClasificacionCreate(BaseModel):
    corriente_id: str
    nombre: str
    descripcion: Optional[str] = None


class ClasificacionUpdate(BaseModel):
    corriente_id: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None


class ClasificacionOut(BaseModel):
    id: str
    codigo: str
    corriente_id: str
    nombre: str
    descripcion: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Isla ─────────────────────────────────────────────────────────────────────

class IslaCreate(BaseModel):
    sitio_id: str
    sector_id: Optional[str] = None
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None


class IslaUpdate(BaseModel):
    sitio_id: Optional[str] = None
    sector_id: Optional[str] = None
    nombre: Optional[str] = None
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None
    activo: Optional[bool] = None


class IslaOut(BaseModel):
    id: str
    codigo: str
    sitio_id: str
    sector_id: Optional[str] = None
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Tacho ────────────────────────────────────────────────────────────────────

class TachoCreate(BaseModel):
    isla_id: str
    corriente_id: str
    nombre: str
    alias: Optional[str] = None
    color: Optional[str] = None
    capacidad: Optional[Decimal] = None
    unidad_capacidad: Optional[str] = None


class TachoUpdate(BaseModel):
    isla_id: Optional[str] = None
    corriente_id: Optional[str] = None
    nombre: Optional[str] = None
    alias: Optional[str] = None
    color: Optional[str] = None
    capacidad: Optional[Decimal] = None
    unidad_capacidad: Optional[str] = None
    activo: Optional[bool] = None


class TachoOut(BaseModel):
    id: str
    codigo: str
    isla_id: str
    corriente_id: str
    nombre: str
    alias: Optional[str] = None
    color: Optional[str] = None
    capacidad: Optional[Decimal] = None
    unidad_capacidad: Optional[str] = None
    version: int
    reemplazado_por_id: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Nodo ─────────────────────────────────────────────────────────────────────

class NodoCreate(BaseModel):
    sitio_id: str
    sector_id: Optional[str] = None
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None


class NodoUpdate(BaseModel):
    sitio_id: Optional[str] = None
    sector_id: Optional[str] = None
    nombre: Optional[str] = None
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None
    activo: Optional[bool] = None


class NodoOut(BaseModel):
    id: str
    codigo: str
    sitio_id: str
    sector_id: Optional[str] = None
    nombre: str
    alias: Optional[str] = None
    descripcion: Optional[str] = None
    latitud: Optional[Decimal] = None
    longitud: Optional[Decimal] = None
    ubicacion_descriptiva: Optional[str] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Vehiculo ─────────────────────────────────────────────────────────────────

class VehiculoCreate(BaseModel):
    patente: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    capacidad_kg: Optional[Decimal] = None


class VehiculoUpdate(BaseModel):
    patente: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    capacidad_kg: Optional[Decimal] = None
    activo: Optional[bool] = None


class VehiculoOut(BaseModel):
    id: str
    codigo: str
    patente: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    capacidad_kg: Optional[Decimal] = None
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Receptor ─────────────────────────────────────────────────────────────────

class ReceptorCreate(BaseModel):
    nombre: str
    tipo: str = "otro"
    descripcion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    cuit: Optional[str] = None
    contacto_nombre: Optional[str] = None
    es_provisorio: bool = False


class ReceptorUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    cuit: Optional[str] = None
    contacto_nombre: Optional[str] = None
    es_provisorio: Optional[bool] = None
    activo: Optional[bool] = None


class ReceptorOut(BaseModel):
    id: str
    codigo: str
    nombre: str
    tipo: str
    descripcion: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    cuit: Optional[str] = None
    contacto_nombre: Optional[str] = None
    es_provisorio: bool
    activo: bool
    created_at: datetime
    updated_at: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


# ─── QRCode ───────────────────────────────────────────────────────────────────

class QRGenerar(BaseModel):
    entidad_tipo: str  # tacho, isla, nodo
    entidad_id: str


class QRCodeOut(BaseModel):
    id: str
    entidad_tipo: str
    entidad_id: str
    codigo_qr: str
    url_qr: str
    activo: bool
    generado_at: datetime
    generado_por: Optional[str] = None

    class Config:
        from_attributes = True


# ─── Documento ────────────────────────────────────────────────────────────────

class DocumentoOut(BaseModel):
    id: str
    entidad_tipo: str
    entidad_id: str
    nombre_archivo: str
    tipo_mime: Optional[str] = None
    ruta_archivo: str
    descripcion: Optional[str] = None
    activo: bool
    uploaded_at: datetime
    uploaded_by: Optional[str] = None

    class Config:
        from_attributes = True
