import React, { useState, useEffect } from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

export default function IslasPage() {
  const [sitiosOptions, setSitiosOptions] = useState([])
  const [sectoresOptions, setSectoresOptions] = useState([])

  useEffect(() => {
    api.sitios.list({ activo: true, limit: 500 })
      .then(data => {
        const arr = Array.isArray(data) ? data : (data.items || [])
        setSitiosOptions(arr.map(s => ({ value: s.id, label: `${s.codigo} - ${s.nombre}` })))
      })
    api.sectores.list({ activo: true, limit: 1000 })
      .then(data => {
        const arr = Array.isArray(data) ? data : (data.items || [])
        setSectoresOptions(arr.map(s => ({ value: s.id, label: `${s.codigo} - ${s.nombre}` })))
      })
  }, [])

  const COLUMNS = [
    { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
    { key: 'nombre', label: 'Nombre' },
    { key: 'alias', label: 'Alias' },
    { key: 'latitud', label: 'Lat' },
    { key: 'longitud', label: 'Long' },
  ]

  const FIELDS = [
    { key: 'sitio_id', label: 'Sitio', required: true, type: 'select', options: sitiosOptions },
    { key: 'sector_id', label: 'Sector (opcional)', type: 'select', options: sectoresOptions },
    { key: 'nombre', label: 'Nombre', required: true },
    { key: 'alias', label: 'Alias' },
    { key: 'descripcion', label: 'Descripción', type: 'textarea' },
    { key: 'latitud', label: 'Latitud', type: 'number' },
    { key: 'longitud', label: 'Longitud', type: 'number' },
    { key: 'ubicacion_descriptiva', label: 'Ubicación descriptiva', type: 'textarea' },
  ]

  return (
    <CrudTable
      title="Islas"
      api={api.islas}
      columns={COLUMNS}
      fields={FIELDS}
      exportUrl="/api/exportar/islas"
    />
  )
}
