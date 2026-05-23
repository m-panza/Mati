import uuid
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    Enum as SAEnum,
    Numeric,
    Integer,
    Text,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


def _uuid():
    return str(uuid.uuid4())


def _now():
    return datetime.now(timezone.utc)


class Persona(Base):
    __tablename__ = "personas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)
    documento_tipo: Mapped[str | None] = mapped_column(String(20), nullable=True)
    documento_nro: Mapped[str | None] = mapped_column(String(50), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Sitio(Base):
    __tablename__ = "sitios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    direccion: Mapped[str | None] = mapped_column(String(300), nullable=True)
    localidad: Mapped[str | None] = mapped_column(String(100), nullable=True)
    provincia: Mapped[str | None] = mapped_column(String(100), nullable=True)
    latitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    ubicacion_descriptiva: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Sector(Base):
    __tablename__ = "sectores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    sitio_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sitios.id", ondelete="RESTRICT"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Corriente(Base):
    __tablename__ = "corrientes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Clasificacion(Base):
    __tablename__ = "clasificaciones"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    corriente_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("corrientes.id", ondelete="RESTRICT"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Isla(Base):
    __tablename__ = "islas"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    sitio_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sitios.id", ondelete="RESTRICT"), nullable=False
    )
    sector_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("sectores.id", ondelete="SET NULL"), nullable=True
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    ubicacion_descriptiva: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Tacho(Base):
    __tablename__ = "tachos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    isla_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("islas.id", ondelete="RESTRICT"), nullable=False
    )
    corriente_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("corrientes.id", ondelete="RESTRICT"), nullable=False
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    color: Mapped[str | None] = mapped_column(String(20), nullable=True)
    capacidad: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    unidad_capacidad: Mapped[str | None] = mapped_column(String(20), nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    reemplazado_por_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("tachos.id", ondelete="SET NULL"), nullable=True
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Nodo(Base):
    __tablename__ = "nodos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    sitio_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("sitios.id", ondelete="RESTRICT"), nullable=False
    )
    sector_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("sectores.id", ondelete="SET NULL"), nullable=True
    )
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    alias: Mapped[str | None] = mapped_column(String(100), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    latitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    ubicacion_descriptiva: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class IslaNodo(Base):
    __tablename__ = "islas_nodos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    isla_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("islas.id", ondelete="RESTRICT"), nullable=False
    )
    nodo_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("nodos.id", ondelete="RESTRICT"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )


class NodoCorriente(Base):
    __tablename__ = "nodos_corrientes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    nodo_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("nodos.id", ondelete="RESTRICT"), nullable=False
    )
    corriente_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("corrientes.id", ondelete="RESTRICT"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )


class Vehiculo(Base):
    __tablename__ = "vehiculos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    patente: Mapped[str | None] = mapped_column(String(20), nullable=True)
    tipo: Mapped[str | None] = mapped_column(String(50), nullable=True)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    capacidad_kg: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Receptor(Base):
    __tablename__ = "receptores"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(200), nullable=False)
    tipo: Mapped[str] = mapped_column(
        SAEnum(
            "cooperativa",
            "fundacion",
            "organizacion",
            "operador",
            "proveedor",
            "otro",
            name="receptor_tipo",
        ),
        nullable=False,
        default="otro",
    )
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    telefono: Mapped[str | None] = mapped_column(String(50), nullable=True)
    direccion: Mapped[str | None] = mapped_column(String(300), nullable=True)
    cuit: Mapped[str | None] = mapped_column(String(20), nullable=True)
    contacto_nombre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    es_provisorio: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class ReceptorCorriente(Base):
    __tablename__ = "receptores_corrientes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    receptor_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("receptores.id", ondelete="RESTRICT"), nullable=False
    )
    corriente_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("corrientes.id", ondelete="RESTRICT"), nullable=False
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )


class PersonaAsignacion(Base):
    __tablename__ = "personas_asignaciones"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    persona_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("personas.id", ondelete="RESTRICT"), nullable=False
    )
    entidad_tipo: Mapped[str] = mapped_column(
        SAEnum("sitio", "isla", "nodo", name="entidad_tipo_enum"), nullable=False
    )
    entidad_id: Mapped[str] = mapped_column(String(36), nullable=False)
    rol_asignacion: Mapped[str] = mapped_column(
        SAEnum(
            "responsable", "suplente", "operador", name="rol_asignacion_enum"
        ),
        nullable=False,
        default="operador",
    )
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    created_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class QRCode(Base):
    __tablename__ = "qrcodes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    entidad_tipo: Mapped[str] = mapped_column(
        SAEnum("tacho", "isla", "nodo", name="qr_entidad_tipo_enum"), nullable=False
    )
    entidad_id: Mapped[str] = mapped_column(String(36), nullable=False)
    codigo_qr: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    url_qr: Mapped[str] = mapped_column(String(500), nullable=False)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    generado_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    generado_por: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Documento(Base):
    __tablename__ = "documentos"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    entidad_tipo: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad_id: Mapped[str] = mapped_column(String(36), nullable=False)
    nombre_archivo: Mapped[str] = mapped_column(String(300), nullable=False)
    tipo_mime: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ruta_archivo: Mapped[str] = mapped_column(String(500), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    uploaded_by: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )


class Auditoria(Base):
    __tablename__ = "auditoria"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    tabla: Mapped[str] = mapped_column(String(100), nullable=False)
    registro_id: Mapped[str] = mapped_column(String(36), nullable=False)
    accion: Mapped[str] = mapped_column(String(20), nullable=False)
    campo: Mapped[str | None] = mapped_column(String(100), nullable=True)
    valor_anterior: Mapped[str | None] = mapped_column(Text, nullable=True)
    valor_nuevo: Mapped[str | None] = mapped_column(Text, nullable=True)
    usuario_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    usuario_email: Mapped[str] = mapped_column(String(255), nullable=False)
    ip: Mapped[str | None] = mapped_column(String(50), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
