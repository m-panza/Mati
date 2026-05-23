import React, { useState, useEffect } from 'react'
import { api } from '../api/client'
import MapView from '../components/MapView'

const ENTITIES = [
  { key: 'sitios', label: 'Sitios' },
  { key: 'sectores', label: 'Sectores' },
  { key: 'corrientes', label: 'Corrientes' },
  { key: 'islas', label: 'Islas' },
  { key: 'tachos', label: 'Tachos' },
  { key: 'nodos', label: 'Nodos' },
  { key: 'vehiculos', label: 'Vehículos' },
  { key: 'receptores', label: 'Receptores' },
  { key: 'personas', label: 'Personas' },
]

export default function DashboardPage() {
  const [counts, setCounts] = useState({})
  const [sitios, setSitios] = useState([])
  const [islas, setIslas] = useState([])
  const [nodos, setNodos] = useState([])

  useEffect(() => {
    // Fetch counts
    ENTITIES.forEach(({ key }) => {
      api[key].list({ activo: true, limit: 1000 })
        .then(data => {
          const arr = Array.isArray(data) ? data : (data.items || [])
          setCounts(prev => ({ ...prev, [key]: arr.length }))
        })
        .catch(() => {})
    })

    // Fetch map data
    api.sitios.list({ activo: true, limit: 200 }).then(data => {
      setSitios(Array.isArray(data) ? data : (data.items || []))
    }).catch(() => {})

    api.islas.list({ activo: true, limit: 500 }).then(data => {
      setIslas(Array.isArray(data) ? data : (data.items || []))
    }).catch(() => {})

    api.nodos.list({ activo: true, limit: 500 }).then(data => {
      setNodos(Array.isArray(data) ? data : (data.items || []))
    }).catch(() => {})
  }, [])

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Dashboard</h1>
      </div>

      <div className="stats-grid">
        {ENTITIES.map(({ key, label }) => (
          <div key={key} className="stat-card">
            <div className="stat-label">{label}</div>
            <div className="stat-value">{counts[key] ?? '…'}</div>
          </div>
        ))}
      </div>

      <div className="card" style={{ marginBottom: '24px' }}>
        <div style={{ marginBottom: '12px', fontWeight: '600', fontSize: '14px' }}>Mapa de ubicaciones</div>
        <MapView sitios={sitios} islas={islas} nodos={nodos} height="420px" />
      </div>
    </div>
  )
}
