import React from 'react'
import CrudTable from '../components/CrudTable'
import { api } from '../api/client'

const COLUMNS = [
  { key: 'codigo', label: 'Código', render: r => <span className="mono">{r.codigo}</span> },
  { key: 'patente', label: 'Patente' },
  { key: 'tipo', label: 'Tipo' },
  { key: 'capacidad_kg', label: 'Cap. (kg)' },
  { key: 'descripcion', label: 'Descripción' },
]

const FIELDS = [
  { key: 'patente', label: 'Patente' },
  { key: 'tipo', label: 'Tipo' },
  { key: 'descripcion', label: 'Descripción', type: 'textarea' },
  { key: 'capacidad_kg', label: 'Capacidad (kg)', type: 'number' },
]

export default function VehiculosPage() {
  return (
    <CrudTable
      title="Vehículos"
      api={api.vehiculos}
      columns={COLUMNS}
      fields={FIELDS}
      exportUrl="/api/exportar/vehiculos"
    />
  )
}
