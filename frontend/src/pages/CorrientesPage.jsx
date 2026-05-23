import React from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

const COLUMNS = [
  { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
  { key: 'nombre', label: 'Nombre' },
  { key: 'alias', label: 'Alias' },
  {
    key: 'color', label: 'Color',
    render: r => r.color ? (
      <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
        <span style={{ width: '14px', height: '14px', borderRadius: '3px', background: r.color, display: 'inline-block', border: '1px solid var(--border-2)' }} />
        {r.color}
      </span>
    ) : '-'
  },
]

const FIELDS = [
  { key: 'nombre', label: 'Nombre', required: true },
  { key: 'alias', label: 'Alias' },
  { key: 'descripcion', label: 'Descripción', type: 'textarea' },
  { key: 'color', label: 'Color (hex)', placeholder: '#3b82f6' },
]

export default function CorrientesPage() {
  return (
    <CrudTable
      title="Corrientes"
      api={api.corrientes}
      columns={COLUMNS}
      fields={FIELDS}
    />
  )
}
