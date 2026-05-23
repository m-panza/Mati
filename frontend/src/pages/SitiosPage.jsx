import React from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

const COLUMNS = [
  { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
  { key: 'nombre', label: 'Nombre' },
  { key: 'alias', label: 'Alias' },
  { key: 'localidad', label: 'Localidad' },
  { key: 'provincia', label: 'Provincia' },
  { key: 'latitud', label: 'Lat' },
  { key: 'longitud', label: 'Long' },
]

const FIELDS = [
  { key: 'nombre', label: 'Nombre', required: true },
  { key: 'alias', label: 'Alias' },
  { key: 'descripcion', label: 'Descripción', type: 'textarea' },
  { key: 'direccion', label: 'Dirección' },
  { key: 'localidad', label: 'Localidad' },
  { key: 'provincia', label: 'Provincia' },
  { key: 'latitud', label: 'Latitud', type: 'number' },
  { key: 'longitud', label: 'Longitud', type: 'number' },
  { key: 'ubicacion_descriptiva', label: 'Ubicación descriptiva', type: 'textarea' },
]

export default function SitiosPage() {
  return (
    <CrudTable
      title="Sitios"
      api={api.sitios}
      columns={COLUMNS}
      fields={FIELDS}
      exportUrl="/api/exportar/sitios"
    />
  )
}
