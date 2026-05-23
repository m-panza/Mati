import React, { useState, useEffect } from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

export default function TachosPage() {
  const [islasOptions, setIslasOptions] = useState([])
  const [corrientesOptions, setCorrientesOptions] = useState([])

  useEffect(() => {
    api.islas.list({ activo: true, limit: 1000 })
      .then(data => {
        const arr = Array.isArray(data) ? data : (data.items || [])
        setIslasOptions(arr.map(i => ({ value: i.id, label: `${i.codigo} - ${i.nombre}` })))
      })
    api.corrientes.list({ activo: true, limit: 500 })
      .then(data => {
        const arr = Array.isArray(data) ? data : (data.items || [])
        setCorrientesOptions(arr.map(c => ({ value: c.id, label: `${c.codigo} - ${c.nombre}` })))
      })
  }, [])

  const COLUMNS = [
    { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
    { key: 'nombre', label: 'Nombre' },
    { key: 'alias', label: 'Alias' },
    { key: 'version', label: 'Ver.' },
    {
      key: 'color', label: 'Color',
      render: r => r.color ? (
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: '14px', height: '14px', borderRadius: '3px', background: r.color, display: 'inline-block', border: '1px solid var(--border-2)' }} />
          {r.color}
        </span>
      ) : '-'
    },
    { key: 'capacidad', label: 'Cap.' },
    { key: 'unidad_capacidad', label: 'Unidad' },
  ]

  const FIELDS = [
    { key: 'isla_id', label: 'Isla', required: true, type: 'select', options: islasOptions },
    { key: 'corriente_id', label: 'Corriente', required: true, type: 'select', options: corrientesOptions },
    { key: 'nombre', label: 'Nombre', required: true },
    { key: 'alias', label: 'Alias' },
    { key: 'color', label: 'Color', placeholder: '#22c55e' },
    { key: 'capacidad', label: 'Capacidad', type: 'number' },
    { key: 'unidad_capacidad', label: 'Unidad de capacidad', placeholder: 'litros, kg, m3...' },
  ]

  return (
    <CrudTable
      title="Tachos"
      api={api.tachos}
      columns={COLUMNS}
      fields={FIELDS}
      exportUrl="/api/exportar/tachos"
    />
  )
}
