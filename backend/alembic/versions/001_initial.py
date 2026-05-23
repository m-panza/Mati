"""Initial schema - create all tables

Revision ID: 001
Revises:
Create Date: 2026-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Tipos definidos con create_type=False — se crean manualmente abajo con checkfirst
user_rol_t         = postgresql.ENUM('admin', 'supervisor', 'operador', 'visualizador',  name='user_rol',            create_type=False)
receptor_tipo_t    = postgresql.ENUM('cooperativa', 'fundacion', 'organizacion', 'operador', 'proveedor', 'otro',     name='receptor_tipo',       create_type=False)
entidad_tipo_t     = postgresql.ENUM('sitio', 'isla', 'nodo',                                                         name='entidad_tipo_enum',   create_type=False)
rol_asignacion_t   = postgresql.ENUM('responsable', 'suplente', 'operador',                                           name='rol_asignacion_enum', create_type=False)
qr_entidad_tipo_t  = postgresql.ENUM('tacho', 'isla', 'nodo',                                                         name='qr_entidad_tipo_enum',create_type=False)


def upgrade() -> None:
    bind = op.get_bind()

    # Crear tipos ENUM con checkfirst=True (idempotente)
    user_rol_t.create(bind, checkfirst=True)
    receptor_tipo_t.create(bind, checkfirst=True)
    entidad_tipo_t.create(bind, checkfirst=True)
    rol_asignacion_t.create(bind, checkfirst=True)
    qr_entidad_tipo_t.create(bind, checkfirst=True)

    op.create_table(
        'users',
        sa.Column('id',            sa.String(36),   primary_key=True),
        sa.Column('email',         sa.String(255),  nullable=False, unique=True),
        sa.Column('nombre',        sa.String(100),  nullable=False),
        sa.Column('apellido',      sa.String(100),  nullable=False),
        sa.Column('password_hash', sa.String(255),  nullable=False),
        sa.Column('rol',           user_rol_t,      nullable=False),
        sa.Column('activo',        sa.Boolean(),    nullable=False, server_default='true'),
        sa.Column('created_at',    sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',    sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'personas',
        sa.Column('id',             sa.String(36),  primary_key=True),
        sa.Column('codigo',         sa.String(20),  nullable=False, unique=True),
        sa.Column('nombre',         sa.String(100), nullable=False),
        sa.Column('apellido',       sa.String(100), nullable=False),
        sa.Column('email',          sa.String(255), nullable=True),
        sa.Column('telefono',       sa.String(50),  nullable=True),
        sa.Column('documento_tipo', sa.String(20),  nullable=True),
        sa.Column('documento_nro',  sa.String(50),  nullable=True),
        sa.Column('activo',         sa.Boolean(),   nullable=False, server_default='true'),
        sa.Column('created_at',     sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',     sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',     sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'sitios',
        sa.Column('id',                   sa.String(36),    primary_key=True),
        sa.Column('codigo',               sa.String(20),    nullable=False, unique=True),
        sa.Column('nombre',               sa.String(200),   nullable=False),
        sa.Column('alias',                sa.String(100),   nullable=True),
        sa.Column('descripcion',          sa.Text(),        nullable=True),
        sa.Column('direccion',            sa.String(300),   nullable=True),
        sa.Column('localidad',            sa.String(100),   nullable=True),
        sa.Column('provincia',            sa.String(100),   nullable=True),
        sa.Column('latitud',              sa.Numeric(10,7), nullable=True),
        sa.Column('longitud',             sa.Numeric(10,7), nullable=True),
        sa.Column('ubicacion_descriptiva',sa.Text(),        nullable=True),
        sa.Column('activo',               sa.Boolean(),     nullable=False, server_default='true'),
        sa.Column('created_at',           sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',           sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',           sa.String(36),    sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'sectores',
        sa.Column('id',          sa.String(36),  primary_key=True),
        sa.Column('codigo',      sa.String(20),  nullable=False, unique=True),
        sa.Column('sitio_id',    sa.String(36),  sa.ForeignKey('sitios.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('nombre',      sa.String(200), nullable=False),
        sa.Column('alias',       sa.String(100), nullable=True),
        sa.Column('descripcion', sa.Text(),      nullable=True),
        sa.Column('activo',      sa.Boolean(),   nullable=False, server_default='true'),
        sa.Column('created_at',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',  sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'corrientes',
        sa.Column('id',          sa.String(36),  primary_key=True),
        sa.Column('codigo',      sa.String(20),  nullable=False, unique=True),
        sa.Column('nombre',      sa.String(200), nullable=False),
        sa.Column('alias',       sa.String(100), nullable=True),
        sa.Column('descripcion', sa.Text(),      nullable=True),
        sa.Column('color',       sa.String(20),  nullable=True),
        sa.Column('activo',      sa.Boolean(),   nullable=False, server_default='true'),
        sa.Column('created_at',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',  sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'clasificaciones',
        sa.Column('id',           sa.String(36),  primary_key=True),
        sa.Column('codigo',       sa.String(20),  nullable=False, unique=True),
        sa.Column('corriente_id', sa.String(36),  sa.ForeignKey('corrientes.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('nombre',       sa.String(200), nullable=False),
        sa.Column('descripcion',  sa.Text(),      nullable=True),
        sa.Column('activo',       sa.Boolean(),   nullable=False, server_default='true'),
        sa.Column('created_at',   sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',   sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',   sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'islas',
        sa.Column('id',                    sa.String(36),    primary_key=True),
        sa.Column('codigo',                sa.String(20),    nullable=False, unique=True),
        sa.Column('sitio_id',              sa.String(36),    sa.ForeignKey('sitios.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('sector_id',             sa.String(36),    sa.ForeignKey('sectores.id', ondelete='SET NULL'), nullable=True),
        sa.Column('nombre',                sa.String(200),   nullable=False),
        sa.Column('alias',                 sa.String(100),   nullable=True),
        sa.Column('descripcion',           sa.Text(),        nullable=True),
        sa.Column('latitud',               sa.Numeric(10,7), nullable=True),
        sa.Column('longitud',              sa.Numeric(10,7), nullable=True),
        sa.Column('ubicacion_descriptiva', sa.Text(),        nullable=True),
        sa.Column('activo',                sa.Boolean(),     nullable=False, server_default='true'),
        sa.Column('created_at',            sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',            sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',            sa.String(36),    sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'tachos',
        sa.Column('id',               sa.String(36),    primary_key=True),
        sa.Column('codigo',           sa.String(20),    nullable=False, unique=True),
        sa.Column('isla_id',          sa.String(36),    sa.ForeignKey('islas.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('corriente_id',     sa.String(36),    sa.ForeignKey('corrientes.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('nombre',           sa.String(200),   nullable=False),
        sa.Column('alias',            sa.String(100),   nullable=True),
        sa.Column('color',            sa.String(20),    nullable=True),
        sa.Column('capacidad',        sa.Numeric(10,2), nullable=True),
        sa.Column('unidad_capacidad', sa.String(20),    nullable=True),
        sa.Column('version',          sa.Integer(),     nullable=False, server_default='1'),
        sa.Column('reemplazado_por_id', sa.String(36),  sa.ForeignKey('tachos.id', ondelete='SET NULL'), nullable=True),
        sa.Column('activo',           sa.Boolean(),     nullable=False, server_default='true'),
        sa.Column('created_at',       sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',       sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',       sa.String(36),    sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'nodos',
        sa.Column('id',                    sa.String(36),    primary_key=True),
        sa.Column('codigo',                sa.String(20),    nullable=False, unique=True),
        sa.Column('sitio_id',              sa.String(36),    sa.ForeignKey('sitios.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('sector_id',             sa.String(36),    sa.ForeignKey('sectores.id', ondelete='SET NULL'), nullable=True),
        sa.Column('nombre',                sa.String(200),   nullable=False),
        sa.Column('alias',                 sa.String(100),   nullable=True),
        sa.Column('descripcion',           sa.Text(),        nullable=True),
        sa.Column('latitud',               sa.Numeric(10,7), nullable=True),
        sa.Column('longitud',              sa.Numeric(10,7), nullable=True),
        sa.Column('ubicacion_descriptiva', sa.Text(),        nullable=True),
        sa.Column('activo',                sa.Boolean(),     nullable=False, server_default='true'),
        sa.Column('created_at',            sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',            sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',            sa.String(36),    sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'islas_nodos',
        sa.Column('id',         sa.String(36), primary_key=True),
        sa.Column('isla_id',    sa.String(36), sa.ForeignKey('islas.id',  ondelete='RESTRICT'), nullable=False),
        sa.Column('nodo_id',    sa.String(36), sa.ForeignKey('nodos.id',  ondelete='RESTRICT'), nullable=False),
        sa.Column('activo',     sa.Boolean(),  nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'nodos_corrientes',
        sa.Column('id',           sa.String(36), primary_key=True),
        sa.Column('nodo_id',      sa.String(36), sa.ForeignKey('nodos.id',      ondelete='RESTRICT'), nullable=False),
        sa.Column('corriente_id', sa.String(36), sa.ForeignKey('corrientes.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('activo',       sa.Boolean(),  nullable=False, server_default='true'),
        sa.Column('created_at',   sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'vehiculos',
        sa.Column('id',           sa.String(36),    primary_key=True),
        sa.Column('codigo',       sa.String(20),    nullable=False, unique=True),
        sa.Column('patente',      sa.String(20),    nullable=True),
        sa.Column('tipo',         sa.String(50),    nullable=True),
        sa.Column('descripcion',  sa.Text(),        nullable=True),
        sa.Column('capacidad_kg', sa.Numeric(10,2), nullable=True),
        sa.Column('activo',       sa.Boolean(),     nullable=False, server_default='true'),
        sa.Column('created_at',   sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',   sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',   sa.String(36),    sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'receptores',
        sa.Column('id',              sa.String(36),  primary_key=True),
        sa.Column('codigo',          sa.String(20),  nullable=False, unique=True),
        sa.Column('nombre',          sa.String(200), nullable=False),
        sa.Column('tipo',            receptor_tipo_t,nullable=False),
        sa.Column('descripcion',     sa.Text(),      nullable=True),
        sa.Column('email',           sa.String(255), nullable=True),
        sa.Column('telefono',        sa.String(50),  nullable=True),
        sa.Column('direccion',       sa.String(300), nullable=True),
        sa.Column('cuit',            sa.String(20),  nullable=True),
        sa.Column('contacto_nombre', sa.String(200), nullable=True),
        sa.Column('es_provisorio',   sa.Boolean(),   nullable=False, server_default='false'),
        sa.Column('activo',          sa.Boolean(),   nullable=False, server_default='true'),
        sa.Column('created_at',      sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at',      sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',      sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'receptores_corrientes',
        sa.Column('id',           sa.String(36), primary_key=True),
        sa.Column('receptor_id',  sa.String(36), sa.ForeignKey('receptores.id',  ondelete='RESTRICT'), nullable=False),
        sa.Column('corriente_id', sa.String(36), sa.ForeignKey('corrientes.id',  ondelete='RESTRICT'), nullable=False),
        sa.Column('activo',       sa.Boolean(),  nullable=False, server_default='true'),
        sa.Column('created_at',   sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        'personas_asignaciones',
        sa.Column('id',             sa.String(36),   primary_key=True),
        sa.Column('persona_id',     sa.String(36),   sa.ForeignKey('personas.id', ondelete='RESTRICT'), nullable=False),
        sa.Column('entidad_tipo',   entidad_tipo_t,  nullable=False),
        sa.Column('entidad_id',     sa.String(36),   nullable=False),
        sa.Column('rol_asignacion', rol_asignacion_t,nullable=False),
        sa.Column('activo',         sa.Boolean(),    nullable=False, server_default='true'),
        sa.Column('created_at',     sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_by',     sa.String(36),   sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'qrcodes',
        sa.Column('id',           sa.String(36),  primary_key=True),
        sa.Column('entidad_tipo', qr_entidad_tipo_t, nullable=False),
        sa.Column('entidad_id',   sa.String(36),  nullable=False),
        sa.Column('codigo_qr',    sa.String(50),  nullable=False, unique=True),
        sa.Column('url_qr',       sa.String(500), nullable=False),
        sa.Column('activo',       sa.Boolean(),   nullable=False, server_default='true'),
        sa.Column('generado_at',  sa.DateTime(timezone=True), nullable=False),
        sa.Column('generado_por', sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'documentos',
        sa.Column('id',             sa.String(36),  primary_key=True),
        sa.Column('entidad_tipo',   sa.String(50),  nullable=False),
        sa.Column('entidad_id',     sa.String(36),  nullable=False),
        sa.Column('nombre_archivo', sa.String(300), nullable=False),
        sa.Column('tipo_mime',      sa.String(100), nullable=True),
        sa.Column('ruta_archivo',   sa.String(500), nullable=False),
        sa.Column('descripcion',    sa.Text(),      nullable=True),
        sa.Column('activo',         sa.Boolean(),   nullable=False, server_default='true'),
        sa.Column('uploaded_at',    sa.DateTime(timezone=True), nullable=False),
        sa.Column('uploaded_by',    sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
    )

    op.create_table(
        'auditoria',
        sa.Column('id',             sa.String(36),  primary_key=True),
        sa.Column('tabla',          sa.String(100), nullable=False),
        sa.Column('registro_id',    sa.String(36),  nullable=False),
        sa.Column('accion',         sa.String(20),  nullable=False),
        sa.Column('campo',          sa.String(100), nullable=True),
        sa.Column('valor_anterior', sa.Text(),      nullable=True),
        sa.Column('valor_nuevo',    sa.Text(),      nullable=True),
        sa.Column('usuario_id',     sa.String(36),  sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('usuario_email',  sa.String(255), nullable=False),
        sa.Column('ip',             sa.String(50),  nullable=True),
        sa.Column('timestamp',      sa.DateTime(timezone=True), nullable=False),
        sa.Column('descripcion',    sa.Text(),      nullable=True),
    )


def downgrade() -> None:
    op.drop_table('auditoria')
    op.drop_table('documentos')
    op.drop_table('qrcodes')
    op.drop_table('personas_asignaciones')
    op.drop_table('receptores_corrientes')
    op.drop_table('receptores')
    op.drop_table('vehiculos')
    op.drop_table('nodos_corrientes')
    op.drop_table('islas_nodos')
    op.drop_table('nodos')
    op.drop_table('tachos')
    op.drop_table('islas')
    op.drop_table('clasificaciones')
    op.drop_table('corrientes')
    op.drop_table('sectores')
    op.drop_table('sitios')
    op.drop_table('personas')
    op.drop_table('users')
    bind = op.get_bind()
    qr_entidad_tipo_t.drop(bind, checkfirst=True)
    rol_asignacion_t.drop(bind, checkfirst=True)
    entidad_tipo_t.drop(bind, checkfirst=True)
    receptor_tipo_t.drop(bind, checkfirst=True)
    user_rol_t.drop(bind, checkfirst=True)
