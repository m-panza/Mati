import React, { useState, useEffect } from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

export default function SectoresPage() {
  const [sitiosOptions, setSitiosOptions] = useState([])

  useEffect(() => {
    api.sitios.list({ activo: true, limit: 500 })
      .then(data => {
        const arr = Array.isArray(data) ? data : (data.items || [])
        setSitiosOptions(arr.map(s => ({ value: s.id, label: `${s.codigo} - ${s.nombre}` })))
      })
      .catch(() => {})
  }, [])

  const COLUMNS = [
    { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
    { key: 'nombre', label: 'Nombre' },
    { key: 'alias', label: 'Alias' },
    { key: 'sitio_id', label: 'Sitio ID', render: r => <span className="mono" style={{ fontSize: '11px' }}>{r.sitio_id}</span> },
  ]

  const FIELDS = [
    { key: 'sitio_id', label: 'Sitio', required: true, type: 'select', options: sitiosOptions },
    { key: 'nombre', label: 'Nombre', required: true },
    { key: 'alias', label: 'Alias' },
    { key: 'descripcion', label: 'Descripción', type: 'textarea' },
  ]

  return (
    <CrudTable
      title="Sectores"
      api={api.sectores}
      columns={COLUMNS}
      fields={FIELDS}
      exportUrl="/api/exportar/sectores"
    />
  )
}
