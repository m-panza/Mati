import React from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

const TIPO_OPTIONS = [
  { value: 'cooperativa', label: 'Cooperativa' },
  { value: 'fundacion', label: 'Fundación' },
  { value: 'organizacion', label: 'Organización' },
  { value: 'operador', label: 'Operador' },
  { value: 'proveedor', label: 'Proveedor' },
  { value: 'otro', label: 'Otro' },
]

const COLUMNS = [
  { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
  { key: 'nombre', label: 'Nombre' },
  { key: 'tipo', label: 'Tipo', render: r => <span className="badge badge-info">{r.tipo}</span> },
  { key: 'email', label: 'Email' },
  { key: 'telefono', label: 'Teléfono' },
  { key: 'cuit', label: 'CUIT' },
  { key: 'contacto_nombre', label: 'Contacto' },
]

const FIELDS = [
  { key: 'nombre', label: 'Nombre', required: true },
  { key: 'tipo', label: 'Tipo', required: true, type: 'select', options: TIPO_OPTIONS },
  { key: 'descripcion', label: 'Descripción', type: 'textarea' },
  { key: 'email', label: 'Email', type: 'email' },
  { key: 'telefono', label: 'Teléfono' },
  { key: 'direccion', label: 'Dirección' },
  { key: 'cuit', label: 'CUIT' },
  { key: 'contacto_nombre', label: 'Nombre de contacto' },
]

export default function ReceptoresPage() {
  return (
    <CrudTable
      title="Receptores"
      api={api.receptores}
      columns={COLUMNS}
      fields={FIELDS}
      exportUrl="/api/exportar/receptores"
    />
  )
}
