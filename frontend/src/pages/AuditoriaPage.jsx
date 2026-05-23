import React, { useState, useEffect, useCallback } from 'react'
import { authFetch } from '../api/client'

const BASE_URL = import.meta.env.VITE_API_URL || '/api'

const ACCIONES = ['', 'CREATE', 'UPDATE', 'DEACTIVATE', 'REACTIVATE']
const TABLAS = ['', 'users', 'sitios', 'sectores', 'corrientes', 'clasificaciones',
  'islas', 'tachos', 'nodos', 'vehiculos', 'receptores', 'personas', 'qrcodes', 'documentos']

async function fetchAuditoria(params = {}) {
  const qs = new URLSearchParams(
    Object.entries(params).filter(([, v]) => v !== undefined && v !== null && v !== '')
  ).toString()
  const res = await authFetch(`/auditoria${qs ? '?' + qs : ''}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}

export default function AuditoriaPage() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [tabla, setTabla] = useState('')
  const [accion, setAccion] = useState('')
  const [fechaDesde, setFechaDesde] = useState('')
  const [fechaHasta, setFechaHasta] = useState('')

  const load = useCallback(() => {
    setLoading(true)
    fetchAuditoria({ tabla, accion, fecha_desde: fechaDesde, fecha_hasta: fechaHasta, limit: 500 })
      .then(data => setItems(Array.isArray(data) ? data : (data.items || [])))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [tabla, accion, fechaDesde, fechaHasta])

  useEffect(() => { load() }, [load])

  function exportUrl() {
    const p = new URLSearchParams()
    if (tabla) p.set('tabla', tabla)
    if (accion) p.set('accion', accion)
    if (fechaDesde) p.set('fecha_desde', fechaDesde)
    if (fechaHasta) p.set('fecha_hasta', fechaHasta)
    return `${BASE_URL}/exportar/auditoria${p.toString() ? '?' + p.toString() : ''}`
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Auditoría</h1>
        <div className="search-bar" style={{ flexWrap: 'wrap', gap: '8px' }}>
          <select className="search-input" style={{ width: '130px' }} value={tabla} onChange={e => setTabla(e.target.value)}>
            <option value="">Todas las tablas</option>
            {TABLAS.filter(Boolean).map(t => <option key={t} value={t}>{t}</option>)}
          </select>
          <select className="search-input" style={{ width: '130px' }} value={accion} onChange={e => setAccion(e.target.value)}>
            {ACCIONES.map(a => <option key={a} value={a}>{a || 'Todas las acciones'}</option>)}
          </select>
          <input
            type="date"
            className="search-input"
            style={{ width: '150px' }}
            value={fechaDesde}
            onChange={e => setFechaDesde(e.target.value)}
          />
          <input
            type="date"
            className="search-input"
            style={{ width: '150px' }}
            value={fechaHasta}
            onChange={e => setFechaHasta(e.target.value)}
          />
          <a href={exportUrl()} className="btn btn-secondary" style={{ textDecoration: 'none' }} download>↓ CSV</a>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}><span className="spinner" /></div>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Timestamp</th>
                <th>Tabla</th>
                <th>Acción</th>
                <th>Registro ID</th>
                <th>Campo</th>
                <th>Valor Anterior</th>
                <th>Valor Nuevo</th>
                <th>Usuario</th>
                <th>IP</th>
                <th>Descripción</th>
              </tr>
            </thead>
            <tbody>
              {items.length === 0 ? (
                <tr>
                  <td colSpan={10} style={{ textAlign: 'center', color: 'var(--text-2)', padding: '32px' }}>Sin registros</td>
                </tr>
              ) : items.map(row => (
                <tr key={row.id}>
                  <td className="mono" style={{ fontSize: '11px' }}>{new Date(row.timestamp).toLocaleString()}</td>
                  <td><span className="badge badge-info">{row.tabla}</span></td>
                  <td>
                    <span className={`badge ${
                      row.accion === 'CREATE' ? 'badge-success' :
                      row.accion === 'DEACTIVATE' ? 'badge-danger' :
                      'badge-warning'
                    }`}>{row.accion}</span>
                  </td>
                  <td className="mono" style={{ fontSize: '11px', maxWidth: '80px', overflow: 'hidden', textOverflow: 'ellipsis' }}>{row.registro_id}</td>
                  <td>{row.campo || '-'}</td>
                  <td style={{ maxWidth: '120px', overflow: 'hidden', textOverflow: 'ellipsis' }}>{row.valor_anterior || '-'}</td>
                  <td style={{ maxWidth: '120px', overflow: 'hidden', textOverflow: 'ellipsis' }}>{row.valor_nuevo || '-'}</td>
                  <td style={{ fontSize: '12px' }}>{row.usuario_email}</td>
                  <td className="mono" style={{ fontSize: '11px' }}>{row.ip || '-'}</td>
                  <td style={{ maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', fontSize: '12px' }}>{row.descripcion || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
