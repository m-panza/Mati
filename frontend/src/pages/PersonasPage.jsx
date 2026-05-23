import React from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

const COLUMNS = [
  { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
  { key: 'apellido', label: 'Apellido' },
  { key: 'nombre', label: 'Nombre' },
  { key: 'email', label: 'Email' },
  { key: 'telefono', label: 'Teléfono' },
  { key: 'documento_tipo', label: 'Doc. Tipo' },
  { key: 'documento_nro', label: 'Doc. Nro' },
]

const FIELDS = [
  { key: 'nombre', label: 'Nombre', required: true },
  { key: 'apellido', label: 'Apellido', required: true },
  { key: 'email', label: 'Email', type: 'email' },
  { key: 'telefono', label: 'Teléfono' },
  { key: 'documento_tipo', label: 'Tipo de documento', placeholder: 'DNI, Pasaporte...' },
  { key: 'documento_nro', label: 'Nro de documento' },
]

export default function PersonasPage() {
  return (
    <CrudTable
      title="Personas"
      api={api.personas}
      columns={COLUMNS}
      fields={FIELDS}
      exportUrl="/api/exportar/personas"
    />
  )
}
